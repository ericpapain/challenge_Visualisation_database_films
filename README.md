# 🎬 Plateforme d'Exploration Cinématographique (Hi! PARIS)

Bienvenue dans le dépôt de la plateforme d'exploration cinématographique, conçue dans le cadre du test Hi! PARIS. Cette application est un démonstrateur interactif alliant **Exploration Visuelle de données**, **Statistiques (Dataviz)** et **Intelligence Artificielle (RAG & Agent Pandas)**.

---

## 🏗️ Architecture du Système

Pour garantir une base de code propre, modulaire et professionnelle (Software Engineering), l'application ne repose pas sur un simple script monolithique. Elle a été scindée en **4 composants logiques** distincts :

1. 🗄️ **`backend_data.py` (Couche Données)**
   - Charge et nettoie le jeu de données (`movies.csv`).
   - Initialise la base de données vectorielle locale (`FAISS`) pour permettre la recherche sémantique basée sur les synopsis des films.

2. 🧠 **`logic_ai.py` (Couche Intelligence Artificielle)**
   - Le "cerveau" de l'application.
   - Contient le **Routeur d'Intentions** permettant de détecter si l'utilisateur demande une recommandation de film ou génère une question analytique.
   - Gère les appels à l'API LLM (Llama-3) de HuggingFace via le *Prompt Engineering* (Few-Shot, RAG, Follow-up).

3. 🎨 **`frontend_ui.py` (Couche Interface Utilisateur)**
   - Isole tout le code visuel de l'application.
   - Contient l'injection du **CSS personnalisé** aux couleurs de Hi! PARIS (Bleu profond et Rose vif), les animations, la modale d'affichage des détails d'un film et les graphiques statistiques dynamiques `Plotly`.

4. 🚀 **`app.py` (Le Chef d'Orchestre)**
   - Le point d'entrée principal de l'application.
   - Très allégé, il s'occupe de l'affichage de la barre latérale, de l'orchestration des données entre l'UI et l'IA, et de la structure de l'application Streamlit.

---

## 🚀 Comment lancer l'application en local

### 1. Prérequis
Assurez-vous d'avoir installé Python (version recommandée : 3.9+). 
Il est conseillé de créer un environnement virtuel :
```bash
python -m venv venv
# Activation (Windows)
venv\Scripts\activate
# Activation (Mac/Linux)
source venv/bin/activate
```

### 2. Installation des dépendances
Installez toutes les bibliothèques requises pour faire tourner le projet (Streamlit, Pandas, LangChain, FAISS, Plotly, HuggingFace Hub) :
*(Si vous avez un fichier `requirements.txt`, lancez la commande suivante, sinon installez-les manuellement)*
```bash
pip install streamlit pandas langchain langchain-community langchain-huggingface faiss-cpu sentence-transformers plotly seaborn matplotlib
```

### 3. Lancement de l'interface
Lancez le serveur Streamlit localement avec la commande suivante à la racine du projet :
```bash
python -m streamlit run app.py
```
L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

---

## 🔑 Configuration de l'Intelligence Artificielle (HuggingFace)

L'application intègre un **Assistant IA Chatbot** propulsé par des modèles open-source de pointes (comme *Llama-3-8B*). Pour pouvoir lui poser des questions et exécuter des requêtes, vous devez configurer un accès à **HuggingFace**.

### Pourquoi un Token ?
La plateforme utilise le Cloud de HuggingFace (via l'API `HuggingFaceEndpoint`) pour l'inférence de l'Intelligence Artificielle. Un **Token d'accès (API Key)** est obligatoire pour vous authentifier et autoriser les requêtes vers le LLM.

### Comment obtenir votre Token (Gratuit) :
1. Créez un compte gratuit sur [HuggingFace.co](https://huggingface.co/join).
2. Connectez-vous et rendez-vous dans les paramètres (Settings) > **Access Tokens** (ou directement via ce lien : [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)).
3. Cliquez sur **"New token"** ou **"Create new token"**.
4. Donnez un nom à votre token (ex: `streamlit_app`) et sélectionnez le type `Read` (Lecture seule suffit).
5. Copiez la clé secrète générée (qui commence souvent par `hf_...`).

### Où l'insérer dans l'application ?
Une fois l'application Streamlit lancée, ouvrez le panneau latéral gauche (Barre latérale).
Dans la section **"🔑 Configuration IA (LLM)"**, vous verrez un champ `HuggingFace API Key (Token)`. 
Collez simplement votre Token dans ce champ.
*Note : Un token par défaut est pré-rempli dans le code pour la démonstration (au cas où).*

**Dès que le token est renseigné, le bouton flottant (Chatbot rouge clignotant) devient actif en bas à droite de l'écran.** Vous pouvez alors poser vos questions !
