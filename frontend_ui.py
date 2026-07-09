import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def inject_custom_css():
    st.markdown("""
        <style>
        /* =========================================
           REFONTE DES COULEURS - THEME HI! PARIS 
           ========================================= */
           
        /* Fond principal et textes */
        [data-testid="stAppViewContainer"] {
            background-color: #021a3a !important; /* Fond principal bleu très foncé */
        }
        [data-testid="stSidebar"] {
            background-color: #042B59 !important; /* Barre latérale bleu Hi! Paris */
        }
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #FFFFFF !important; /* Force le texte de la barre latérale en blanc */
        }
        
        /* Bouton de fermeture de la sidebar (flèches) */
        div[data-testid="stSidebarCollapseButton"],
        div[data-testid="stSidebarCollapseButton"] button,
        div[data-testid="stSidebarCollapseButton"] span {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        div[data-testid="stSidebarCollapseButton"] {
            animation: pulse-glow 2s infinite !important;
            background-color: rgba(233, 4, 77, 0.8) !important; /* Fond légèrement rouge pour attirer l'oeil */
            border-radius: 50% !important;
        }
        
        /* Titres en Rose/Rouge Hi! Paris */
        h1, h2, h3 {
            color: #E9044D !important;
        }
        /* Boîte pédagogique */
        .pedagogy-box {
            background-color: #042B59;
            padding: 15px;
            border-left: 4px solid #E9044D;
            margin-bottom: 20px;
            font-size: 0.95rem;
            border-radius: 4px;
            color: white;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #042B59 !important;
            border: 1px solid #E9044D !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(233, 4, 77, 0.4);
        }
        /* Force le texte (titres de films, paragraphes, dates) en blanc globalement */
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] strong,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stCaptionContainer"] p,
        div[data-testid="stCaptionContainer"] span {
            color: #FFFFFF !important;
        }
        
        /* Effet de survol robuste sur les affiches de films */
        .movie-card-internal {
            transition: transform 0.3s ease, filter 0.3s ease;
        }
        .movie-card-internal:hover {
            transform: scale(1.03) !important;
        }
        .movie-card-internal:hover img {
            filter: brightness(1.1);
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] p,
        [data-testid="stVerticalBlockBorderWrapper"] span,
        [data-testid="stVerticalBlockBorderWrapper"] strong {
            color: #FFFFFF !important;
        }
        
        /* Boutons standards (Voir les détails, etc.) */
        div.stButton > button {
            background-color: #E9044D !important;
            color: white !important;
            border: 1px solid #E9044D !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: white !important;
            color: #000000 !important; /* Texte du bouton passe en noir au survol */
            transform: scale(1.05);
        }
        
        /* Modale "Voir les détails" (Pop-up) */
        div[role="dialog"], 
        div[data-testid="stDialog"],
        div[data-testid="stModal"] {
            background-color: #FFFFFF !important; /* Fond blanc pour la lisibilité */
        }
        div[role="dialog"] p, div[data-testid="stDialog"] p, div[data-testid="stModal"] p,
        div[role="dialog"] span, div[data-testid="stDialog"] span, div[data-testid="stModal"] span,
        div[role="dialog"] strong, div[data-testid="stDialog"] strong, div[data-testid="stModal"] strong,
        div[role="dialog"] h1, div[data-testid="stDialog"] h1, div[data-testid="stModal"] h1,
        div[role="dialog"] h2, div[data-testid="stDialog"] h2, div[data-testid="stModal"] h2,
        div[role="dialog"] h3, div[data-testid="stDialog"] h3, div[data-testid="stModal"] h3 {
            color: #000000 !important; /* Force le texte de la modale en noir */
        }
        /* Surcharge pour s'assurer que les conteneurs markdown dans la modale sont bien noirs */
        div[role="dialog"] div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stDialog"] div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stModal"] div[data-testid="stMarkdownContainer"] p,
        div[role="dialog"] div[data-testid="stMarkdownContainer"] strong,
        div[data-testid="stDialog"] div[data-testid="stMarkdownContainer"] strong,
        div[data-testid="stModal"] div[data-testid="stMarkdownContainer"] strong,
        div[role="dialog"] div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stDialog"] div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stModal"] div[data-testid="stMarkdownContainer"] span,
        div[role="dialog"] hr, div[data-testid="stDialog"] hr, div[data-testid="stModal"] hr {
            color: #000000 !important;
            border-color: #000000 !important;
        }
        
        /* Personnalisation des bulles du Chatbot pour un texte blanc */
        div[data-testid="stChatMessage"] {
            background-color: #021a3a !important; /* Bleu nuit Hi! Paris */
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* Spécificité MAXIMALE pour forcer le texte en blanc à l'intérieur du chatbot, qu'il soit dans un popover ou une modale */
        div[data-testid="stPopoverBody"] div[data-testid="stChatMessage"],
        div[data-testid="stPopoverBody"] div[data-testid="stChatMessage"] *,
        div[role="dialog"] div[data-testid="stChatMessage"],
        div[role="dialog"] div[data-testid="stChatMessage"] *,
        div[data-testid="stChatMessage"],
        div[data-testid="stChatMessage"] * {
            color: #FFFFFF !important;
        }
        
        /* Onglets */
        .stTabs [data-baseweb="tab-list"] button {
            color: white !important;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab-list"] button p {
            font-size: 32px !important; /* Taille agrandie (réduite de moitié selon votre demande) */
            margin: 0;
            padding: 10px 0;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #E9044D !important;
            border-bottom-color: #E9044D !important;
        }
        
        /* =========================================
           CHATBOT FLOTTANT
           ========================================= */
        @keyframes pulse-glow {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(233, 4, 77, 0.8);
            }
            50% {
                transform: scale(1.05);
                box-shadow: 0 0 0 20px rgba(233, 4, 77, 0);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(233, 4, 77, 0);
            }
        }
        
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 50px !important;
            right: 50px !important;
            z-index: 999999 !important;
            width: auto !important;
            height: auto !important;
            display: inline-block !important;
        }
        div[data-testid="stPopover"] button {
            border-radius: 50% !important;
            width: 80px !important;    /* Taille réduite selon votre demande */
            height: 80px !important;
            background: linear-gradient(135deg, #042B59, #E9044D) !important; /* Dégradé aux couleurs Hi! Paris */
            color: white !important;
            border: 4px solid white !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: transform 0.2s ease;
            animation: pulse-glow 2s infinite !important; /* Animation de clignotement/pulsation */
        }
        div[data-testid="stPopover"] button:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 30px rgba(233, 4, 77, 0.8) !important;
        }
        div[data-testid="stPopover"] button p {
            font-size: 45px !important;  /* Taille de l'icône réduite */
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* Style du texte à l'intérieur du Chatbot (fenêtre) */
        div[data-testid="stPopoverBody"] p,
        div[data-testid="stPopoverBody"] li,
        div[data-testid="stPopoverBody"] span,
        div[data-testid="stPopoverBody"] strong,
        div[data-testid="stPopoverBody"] em,
        div[data-testid="stPopoverBody"] .stMarkdown {
            font-size: 12px !important;
            color: #000000 !important; /* Force le texte du chatbot en noir */
        }
        div[data-testid="stPopoverBody"] h3,
        div[data-testid="stPopoverBody"] h1,
        div[data-testid="stPopoverBody"] h2 {
            font-size: 16px !important;
            color: #000000 !important;
        }
        div[data-testid="stPopoverBody"] pre, 
        div[data-testid="stPopoverBody"] code {
            font-size: 10px !important;
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

@st.dialog("🎬 Détails du Film", width="large")
def show_movie_details(title, poster_url, release_year, vote, votes, genres, overview):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster_url, use_container_width=True)
    with col2:
        st.header(title)
        st.markdown(f"**📅 Année :** {release_year}")
        st.markdown(f"**⭐ Note moyenne :** {vote}/10 ({votes} votes)")
        st.markdown(f"**🎭 Genres :** {genres}")
        st.divider()
        st.subheader("Synopsis")
        st.write(overview)

def render_dashboard_tab(df):
    st.subheader("Analyse Statistique Globale")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top Genres (Plotly)")
        genre_series = df['Genre'].str.split(',', expand=True).stack().str.strip().value_counts().head(10)
        fig_genre = px.bar(
            x=genre_series.values, 
            y=genre_series.index, 
            orientation='h',
            labels={'x': 'Nombre de films', 'y': 'Genre'},
            color_discrete_sequence=['#E9044D']
        )
        fig_genre.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_genre, use_container_width=True)

    with col2:
        st.markdown("### Distribution des Notes (Seaborn)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df, x='Vote_Average', bins=20, kde=True, color='#E9044D', ax=ax)
        ax.set_title('Densité des Notes Moyennes', color='white')
        ax.set_xlabel('Note Moyenne (Vote Average)', color='white')
        ax.set_ylabel('Fréquence', color='white')
        fig.patch.set_facecolor('#0E1117') 
        ax.set_facecolor('#0E1117')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        st.pyplot(fig)
        
    st.markdown("### Matrice de Corrélation (Seaborn)")
    fig2, ax2 = plt.subplots(figsize=(10, 3))
    corr_df = df[['Popularity', 'Vote_Average', 'Vote_Count']].corr()
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', ax=ax2, linewidths=.5)
    fig2.patch.set_facecolor('#0E1117')
    ax2.tick_params(colors='white')
    st.pyplot(fig2)
