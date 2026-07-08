# Document de Synthèse – Visualisation et IA pour Hi! PARIS Playground

## 1. Méthodologie et Choix Techniques

Pour répondre à ce défi technique pour le poste d'**Ingénieur IA Éducation** dans le cadre du temps imparti, nous avons développé une plateforme web interactive avec **Python** et le framework **Streamlit**. 

**Pourquoi cette stack technique ?**
- **Orientation Pédagogique et Data :** Streamlit, combiné à `pandas`, est un standard de l'industrie pour créer des démonstrateurs Data/IA rapides et compréhensibles. Le code est hautement lisible, ce qui est essentiel dans un contexte éducatif où le code peut servir de support d'apprentissage.
- **Reproductibilité :** Le projet s'installe et s'exécute avec deux commandes simples via un environnement virtuel standard (`requirements.txt`), garantissant que n'importe quel utilisateur ou étudiant puisse le reproduire sans friction.
- **Ergonomie Premium :** L'usage de CSS personnalisé injecté au sein de Streamlit a permis de construire des cartes de films visuellement attractives, prouvant qu'il est possible de lier simplicité du code back-end Python et qualité du rendu front-end.

## 2. Fonctionnalités Principales : Explorer, Analyser, Discuter

La plateforme valorise la **multimodalité** de la base de données selon trois axes d'interaction :

- **L'Exploration Visuelle (Galerie) :** 
  L'onglet principal présente les films sous forme de galerie d'images. On y retrouve la dimension **image** (affiches issues de `Poster_Url`), **texte** (Titre, synopsis), et **métriques** (Genres, popularité, note moyenne mise en évidence par des badges visuels). L'utilisateur peut filtrer dynamiquement ces données pour observer les changements en temps réel.

  *(Insérer Figure 1 : Capture de la galerie de films avec ses filtres)*

- **L'Analyse Statistique (Dataviz) :**
  Un second onglet génère des analyses graphiques avancées combinant `Plotly`, `Matplotlib`, et `Seaborn`. Il inclut notamment :
  - Un diagramme en barres dynamique (Plotly) pour la répartition par genres.
  - Un histogramme de distribution de la densité des notes (Matplotlib/Seaborn).
  - Une matrice de corrélation (Heatmap) étudiant les liens entre popularité et notes.

  *(Insérer Figure 2 : Capture de l'onglet Tableau de Bord)*

- **L'Interaction Pédagogique (Chatbot IA) :**
  Un troisième onglet propose une interface conversationnelle. Ce Chatbot permet à l'utilisateur de poser des questions en langage naturel (ex: extraire le film le mieux noté). C'est un **outil d'accessibilité aux données**, idéal dans un contexte éducatif pour permettre à un public non-expert d'interroger une base complexe intuitivement.

## 3. Limites et Améliorations Futures

- **Passage à l'échelle (Scalabilité) :** Le chargement en mémoire via `pandas` est parfait pour la démonstration, mais pour une plateforme éducative à grande échelle, la mise en place d'une base de données relationnelle (PostgreSQL) avec un ORM (SQLAlchemy) et une pagination côté serveur serait nécessaire.
- **IA Avancée (RAG et NLP) :** Le Chatbot actuel repose sur des règles d'extraction basiques (Mockup IA). L'intégration d'un LLM couplé à une architecture RAG (Retrieval-Augmented Generation) permettrait des interactions beaucoup plus profondes, notamment pour résumer les synopsis ou générer des quiz éducatifs sur les films.
- **Accessibilité Universelle :** L'ajout de balises ARIA complètes et d'un support strict des lecteurs d'écran est une amélioration indispensable pour une plateforme à vocation éducative et inclusive.

## 4. Synergie IA et Développement (Pair-Programming)

Dans le cadre de ce challenge, l'usage d'un assistant IA génératif a été centralisé autour du paradigme de **pair-programming**. 
- L'IA a été mobilisée pour accélérer la génération du "boilerplate" Streamlit, la mise en forme du CSS avancé (Dark Mode) et la syntaxe spécifique des graphiques croisés (Seaborn/Matplotlib).
- Le rôle de l'Ingénieur IA a été de **concevoir l'architecture pédagogique** (les 3 onglets : Explorer, Analyser, Interagir), de s'assurer de la viabilité des types de données Pandas, et de valider l'expérience utilisateur finale. Cette approche illustre parfaitement comment l'IA peut démultiplier la productivité technique tout en laissant le pilotage stratégique à l'humain.
