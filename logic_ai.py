import re
import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

GREETINGS = {"bonjour", "salut", "hello", "hi", "hey", "coucou", "bonsoir", "yo", "merci"}

REFERENCE_WORDS = {
    "lesquels", "laquelle", "lequel", "lesquelles",
    "ces", "ceux", "celui", "celle", "celles",
    "recommande", "recommandes", "conseille", "conseilles", "prefere", "preferes",
    "oui", "non", "ok",
    "pourquoi", "explique", "details", "detail",
}

PANDAS_KEYWORDS = {
    "combien", "nombre", "total", "compte", "compter",
    "meilleur", "meilleurs", "top", "classement", "pire", "pires",
    "populaire", "populaires",
    "note", "notes", "moyenne", "superieur", "superieure", "inferieur", "inferieure",
    "annee", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024",
    "langue", "anglais", "francais", "americain", "espagnol", "japonais",
    "trier", "tri", "filtrer", "filtre",
    "statistique", "statistiques", "stats",
    "affiche", "afficher", "montre", "montrer", "liste", "lister", "donne",
    "cherche", "recherche", "trouve", "trouver",
    "genre", "action", "horreur", "comedie", "drame", "thriller", "animation", "romance",
}

def detect_intent(user_q, history):
    """Detecte l'intention de maniere deterministe (sans LLM)."""
    q_lower = user_q.strip().lower()
    q_clean = re.sub(r"[^a-zA-Z0-9\s\u00C0-\u024F']", " ", q_lower)
    q_words = [w for w in q_clean.split() if w]
    
    # 1. Salutations pures
    if len(q_words) <= 3 and any(w in GREETINGS for w in q_words):
        return "GREETING"
    
    # 2. Follow-up : message court avec mots de reference et historique
    has_reference = any(w in REFERENCE_WORDS for w in q_words)
    if has_reference and len(q_words) <= 6 and history:
        return "FOLLOWUP"
    if len(q_words) <= 2 and history:
        return "FOLLOWUP"
    
    # 3. Questions Pandas
    pandas_score = sum(1 for w in q_words if w in PANDAS_KEYWORDS)
    if pandas_score >= 1:
        return "PANDAS"
    
    # 4. Par defaut -> RAG
    return "RAG"

@st.cache_resource
def get_chat_model(api_key, provider="HuggingFace"):
    """Instancie le modèle LLM en fonction du fournisseur choisi."""
    if provider == "Mistral AI":
        return ChatMistralAI(
            model="mistral-small-latest",
            mistral_api_key=api_key,
            temperature=0.1,
            max_tokens=1024
        )
    else:
        # HuggingFace (par défaut)
        llm_endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            huggingfacehub_api_token=api_key,
            temperature=0.1,
            max_new_tokens=1024
        )
        return ChatHuggingFace(llm=llm_endpoint)

def invoke_model(chat_model, prompt):
    response = chat_model.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def get_pandas_prompt(user_q):
    return f"""Tu génères du code Python Pandas. DataFrame = `df`.
Colonnes : Title (str), Release_Date (datetime), Overview (str), Popularity (float), Vote_Count (int), Vote_Average (float), Original_Language (str: 'en','fr','es'...), Genre (str: 'Action, Comedy').

EXEMPLES :
Q: combien de films americain -> len(df[df['Original_Language'] == 'en'])
Q: les 5 meilleurs films -> df.nlargest(5, 'Vote_Average')[['Title', 'Vote_Average']]
Q: meilleurs films de 2020 -> df[df['Release_Date'].dt.year == 2020].nlargest(5, 'Vote_Average')[['Title', 'Vote_Average']]
Q: affiche les films americain -> df[df['Original_Language'] == 'en'][['Title', 'Genre', 'Vote_Average']].head(20)
Q: combien de films au total -> len(df)
Q: combien parle de sexe -> len(df[df['Overview'].str.contains('sex', case=False, na=False)])
Q: films d'horreur -> df[df['Genre'].str.contains('Horror', case=False, na=False)][['Title', 'Genre', 'Vote_Average']].head(20)
Q: films avec note superieure a 8 -> df[df['Vote_Average'] >= 8][['Title', 'Genre', 'Vote_Average']].head(20)
Q: trouve le film Forest -> df[df['Title'].str.contains('Forest', case=False, na=False)][['Title', 'Genre', 'Vote_Average', 'Release_Date']]
Q: films en francais -> df[df['Original_Language'] == 'fr'][['Title', 'Genre', 'Vote_Average']].head(20)
Q: films de genre action -> df[df['Genre'].str.contains('Action', case=False, na=False)][['Title', 'Genre', 'Vote_Average']].head(20)

REGLE ABSOLUE : Réponds UNIQUEMENT avec UNE SEULE LIGNE de code Python. Aucun texte. Aucun commentaire. Aucun markdown.

Question : {user_q}
Code :"""

def get_rag_prompt(user_q, context):
    return f"""Vous êtes un expert cinéphile passionné. L'utilisateur a demandé : "{user_q}"

Voici les 5 films les plus pertinents trouvés par notre moteur de recherche sémantique :
{context}

Instructions :
- Présentez chaque film avec son titre, genre, et note.
- Expliquez POURQUOI chaque film correspond à la demande en vous basant sur le synopsis.
- Si un film ne correspond pas bien, dites-le honnêtement.
- Répondez en français. Soyez complet mais pas trop long."""

def get_followup_prompt(history_text, context_info, user_q):
    return f"""Vous êtes un assistant expert en cinéma. Voici l'historique de la conversation :
{history_text}
{context_info}

L'utilisateur vient de dire : "{user_q}"

Répondez de manière pertinente et utile en vous basant sur l'historique. Si l'utilisateur demande des recommandations, choisissez les meilleurs films parmi ceux déjà mentionnés (basez-vous sur la note et la pertinence). Si on vous demande d'afficher des films, listez-les clairement avec leur titre, genre et note. Soyez naturel."""
