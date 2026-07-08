import streamlit as st
import pandas as pd
import os
import ssl

# ==========================================
# 1. SETUP DE L'ENVIRONNEMENT ET DES IMPORTS
# ==========================================
# Contournement du Proxy d'Entreprise pour éviter l'erreur SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['HF_HUB_DISABLE_SSL_VERIFY'] = '1'

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Hi! PARIS - MovieDB Explorer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports de nos propres modules architecturés
from backend_data import load_data, get_vectorstore, recherche_semantique
from frontend_ui import inject_custom_css, show_movie_details, render_dashboard_tab
from logic_ai import detect_intent, get_chat_model, invoke_model, get_pandas_prompt, get_rag_prompt, get_followup_prompt

# Injection du CSS global
inject_custom_css()

# ==========================================
# 2. INITIALISATION DES DONNÉES ET IA
# ==========================================
with st.spinner("Initialisation du jeu de données..."):
    df = load_data()

all_genres = sorted(list({g.strip() for genres in df['Genre'].dropna() for g in genres.split(',')}))

with st.spinner("Initialisation du RAG Sémantique..."):
    vector_db = get_vectorstore(df)

# ==========================================
# 3. INTERFACE UTILISATEUR : BARRE LATÉRALE
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
st.sidebar.markdown("### 🎓 Démonstrateur IA & Data")
st.sidebar.info("Projet conçu pour illustrer l'accessibilité des données (Hi! PARIS Playground).")

st.sidebar.header("🔑 Configuration IA (LLM)")
hf_api_key = st.sidebar.text_input("HuggingFace API Key (Token)", value="", type="password", help="Obligatoire pour le Chatbot IA")

st.sidebar.header("🔍 Contrôle des données")
search_query = st.sidebar.text_input("Rechercher un film...", "")
selected_genres = st.sidebar.multiselect("Filtrer par Genres", options=all_genres, default=[])
min_vote = st.sidebar.slider("Note Moyenne Minimale", 0.0, 10.0, 0.0, 0.5)
selected_lang = st.sidebar.selectbox("Langue Originale", ["Toutes"] + sorted(df['Original_Language'].unique().tolist()))

# Filtrage dynamique (Pandas)
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(search_query, case=False, na=False)]
if selected_genres:
    pattern = '|'.join(selected_genres)
    filtered_df = filtered_df[filtered_df['Genre'].str.contains(pattern, case=False, na=False)]
if min_vote > 0:
    filtered_df = filtered_df[filtered_df['Vote_Average'] >= min_vote]
if selected_lang != "Toutes":
    filtered_df = filtered_df[filtered_df['Original_Language'] == selected_lang]

# ==========================================
# 4. INTERFACE UTILISATEUR : CONTENU PRINCIPAL
# ==========================================
st.title("🎬 Plateforme d'Exploration Cinématographique")
st.markdown("""
<div class="pedagogy-box">
    <strong>Objectif Pédagogique :</strong> Cette application démontre comment transformer un simple fichier CSV en une expérience interactive. 
    Elle illustre 3 concepts clés : l'exploration visuelle (UI), l'analyse statistique (Dataviz), et une architecture d'Agents (LangChain) pour interroger la donnée.
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🖼️ 1. Exploration Visuelle", "📊 2. Analyse Statistique"])

with tab1:
    st.subheader(f"Résultats : {len(filtered_df):,} films trouvés")
    max_display = st.selectbox("Pagination :", [20, 60, 100], index=1)
    display_df = filtered_df.head(max_display)
    
    cols = st.columns(4)
    for i, (index, row) in enumerate(display_df.iterrows()):
        col = cols[i % 4]
        poster_url = row['Poster_Url'] if pd.notna(row['Poster_Url']) and row['Poster_Url'] != "" else "https://via.placeholder.com/300x450.png?text=No+Poster"
        
        with col:
            with st.container(border=True):
                st.image(poster_url, use_container_width=True)
                st.markdown(f"**{row['Title']}**")
                
                year = row['Release_Date'].year if pd.notna(row['Release_Date']) else 'N/A'
                st.caption(f"📅 {year} | ⭐ {row['Vote_Average']} ({row['Vote_Count']} votes)")
                
                if st.button("Voir les détails", key=f"details_btn_{index}", use_container_width=True):
                    show_movie_details(
                        title=row['Title'],
                        poster_url=poster_url,
                        release_year=year,
                        vote=row['Vote_Average'],
                        votes=row['Vote_Count'],
                        genres=row['Genre'],
                        overview=row.get('Overview', 'Pas de synopsis disponible.')
                    )

with tab2:
    render_dashboard_tab(df)

# ==============================================================
# 5. CHATBOT FLOTTANT ET AGENTS IA
# ==============================================================
if not hf_api_key:
    st.warning("Veuillez entrer votre Token HuggingFace dans la barre latérale pour activer l'Assistant IA.")
else:
    try:
        chat_model = get_chat_model(hf_api_key)
        
        # Etat persistant
        if "messages_agent" not in st.session_state:
            st.session_state.messages_agent = [{"role": "assistant", "content": "🎬 **Assistant Cinéma activé !** Posez-moi vos questions.\n\n**Exemples :**\n- *Quels sont les 5 films les plus populaires ?*\n- *Combien de films d'action y a-t-il ?*\n- *Trouve-moi des films qui parlent de voyages dans le temps*\n- *Films avec une note supérieure à 8*\n- *Trouve le film The Forest of Love*"}]
        if "last_rag_context" not in st.session_state:
            st.session_state.last_rag_context = ""
        if "pending_question" not in st.session_state:
            st.session_state.pending_question = None

        def submit_chat():
            if st.session_state.chat_input_widget:
                user_q = st.session_state.chat_input_widget
                st.session_state.messages_agent.append({"role": "user", "content": user_q})
                st.session_state.pending_question = user_q
                st.session_state.chat_input_widget = ""

        with st.popover("💬", help="Ouvrir l'Assistant IA"):
            st.markdown("### 🤖 Assistant Cinéma IA")
            
            chat_container = st.container(height=400)
            st.text_input("Posez votre question ici...", key="chat_input_widget", on_change=submit_chat, placeholder="Ex: Meilleurs films de 2020...")
            
            with chat_container:
                for idx, msg in enumerate(st.session_state.messages_agent):
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
                        
                        # Afficher le DataFrame persistant s'il y en a un
                        if "dataframe" in msg:
                            res_df = msg["dataframe"]
                            st.dataframe(res_df)
                            
                            if isinstance(res_df, pd.DataFrame) and 'Title' in res_df.columns:
                                movies_list = res_df['Title'].dropna().unique().tolist()
                                if movies_list:
                                    col1, col2 = st.columns([2, 1])
                                    with col1:
                                        selected = st.selectbox(
                                            "Inspecter un film :", 
                                            ["-- Choisissez --"] + movies_list, 
                                            key=f"sel_movie_{idx}"
                                        )
                                    with col2:
                                        if selected != "-- Choisissez --":
                                            st.write("")
                                            st.write("")
                                            if st.button("Voir la fiche", key=f"btn_fiche_{idx}"):
                                                movie_row = df[df['Title'] == selected].iloc[0]
                                                poster = movie_row['Poster_Url'] if pd.notna(movie_row['Poster_Url']) and movie_row['Poster_Url'] != "" else "https://via.placeholder.com/300x450.png?text=No+Poster"
                                                year = movie_row['Release_Date'].year if pd.notna(movie_row['Release_Date']) else 'N/A'
                                                show_movie_details(
                                                    title=movie_row['Title'],
                                                    poster_url=poster,
                                                    release_year=year,
                                                    vote=movie_row['Vote_Average'],
                                                    votes=movie_row['Vote_Count'],
                                                    genres=movie_row['Genre'],
                                                    overview=movie_row.get('Overview', 'Pas de synopsis disponible.')
                                                )
                
                if st.session_state.pending_question:
                    user_q = st.session_state.pending_question
                    with st.chat_message("assistant"):
                        with st.spinner("Analyse en cours..."):
                            try:
                                history_text = ""
                                for msg in st.session_state.messages_agent[-7:-1]:
                                    role_name = "Utilisateur" if msg["role"] == "user" else "Assistant"
                                    history_text += f"{role_name}: {msg['content'][:200]}\n"
                                
                                intent = detect_intent(user_q, st.session_state.messages_agent[1:])
                                
                                if intent == "GREETING":
                                    reply = "Bonjour ! 👋 Je suis votre assistant cinéma. Posez-moi des questions sur notre base de données de films !\n\n**Exemples :**\n- *Quels sont les 5 films les plus populaires ?*\n- *Combien de films d'action y a-t-il ?*\n- *Trouve-moi des films qui parlent d'amour*\n- *Films avec une note supérieure à 8*"
                                    st.markdown(reply)
                                    st.session_state.messages_agent.append({"role": "assistant", "content": reply})
                                    st.session_state.pending_question = None
                                    st.rerun()
                                
                                elif intent == "FOLLOWUP":
                                    context_info = ""
                                    if st.session_state.last_rag_context:
                                        context_info = f"\n\nVoici les derniers films dont nous avons parlé :\n{st.session_state.last_rag_context}"
                                    
                                    followup_prompt = get_followup_prompt(history_text, context_info, user_q)
                                    reply = invoke_model(chat_model, followup_prompt)
                                    st.markdown(reply)
                                    st.session_state.messages_agent.append({"role": "assistant", "content": reply})
                                    st.session_state.pending_question = None
                                    st.rerun()
                                
                                elif intent == "PANDAS":
                                    pandas_prompt = get_pandas_prompt(user_q)
                                    generated_code = invoke_model(chat_model, pandas_prompt)
                                    
                                    if "```" in generated_code:
                                        parts = generated_code.split("```")
                                        for p in parts:
                                            cleaned = p.replace("python", "").strip()
                                            if cleaned.startswith("df") or cleaned.startswith("len("):
                                                generated_code = cleaned
                                                break
                                    generated_code = generated_code.replace("`", "").strip()
                                    
                                    for line in generated_code.split('\n'):
                                        stripped = line.strip()
                                        if stripped and (stripped.startswith("df") or stripped.startswith("len(")):
                                            generated_code = stripped
                                            break
                                    
                                    st.caption(f"📊 Code Pandas : `{generated_code}`")
                                    result = eval(generated_code)
                                    
                                    if isinstance(result, (pd.DataFrame, pd.Series)):
                                        reply = f"Voici le tableau de résultats ({len(result)} éléments) :"
                                        st.session_state.messages_agent.append({
                                            "role": "assistant", 
                                            "content": reply,
                                            "dataframe": result
                                        })
                                    else:
                                        st.metric("Résultat", result)
                                        reply = f"Résultat : **{result}**"
                                        st.session_state.messages_agent.append({"role": "assistant", "content": reply})
                                        
                                    st.session_state.pending_question = None
                                    st.rerun()
                                
                                else:
                                    docs = vector_db.similarity_search(user_q, k=5)
                                    context = ""
                                    for i, doc in enumerate(docs, 1):
                                        context += f"\nFilm {i}:\n{doc.page_content}\n"
                                    
                                    st.session_state.last_rag_context = context
                                    rag_prompt = get_rag_prompt(user_q, context)
                                    
                                    reply = invoke_model(chat_model, rag_prompt)
                                    st.markdown(reply)
                                    st.session_state.messages_agent.append({"role": "assistant", "content": reply})
                                    st.session_state.pending_question = None
                                    st.rerun()
                            
                            except Exception as e:
                                error_str = str(e)
                                if "402" in error_str or "Payment Required" in error_str or "depleted" in error_str:
                                    error_msg = "⚠️ **Crédits API HuggingFace épuisés.** Votre quota mensuel gratuit est atteint."
                                else:
                                    import traceback
                                    error_msg = f"❌ Erreur : {repr(e)}\n\n```\n{traceback.format_exc()}\n```"
                                st.error(error_msg)
                                st.session_state.messages_agent.append({"role": "assistant", "content": error_msg})
                                st.session_state.pending_question = None
                                st.rerun()
                                
    except Exception as e:
        st.error(f"Erreur d'initialisation LLM : {e}")
