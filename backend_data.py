import os
import pandas as pd
import streamlit as st

FAISS_INDEX_PATH = "faiss_index"

@st.cache_data
def load_data() -> pd.DataFrame:
    file_path = "movies.csv"
    if not os.path.exists(file_path):
        file_path = "mymoviedb (1).csv"
    
    try:
        df = pd.read_csv(file_path, parse_dates=['Release_Date'])
    except Exception:
        df = pd.read_csv(file_path, lineterminator='\n')
        df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
        
    df.fillna({'Genre': 'Unknown', 'Original_Language': 'Unknown', 'Overview': 'No overview available.'}, inplace=True)
    return df

@st.cache_resource(show_spinner=False)
def get_vectorstore(_df):
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    if os.path.exists(FAISS_INDEX_PATH):
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        st.info("Construction de l'index RAG (première fois uniquement). Cela peut prendre 1 à 2 minutes...")
        texts = _df.apply(lambda row: f"Titre: {row['Title']}\nGenre: {row['Genre']}\nSynopsis: {row['Overview']}\nDate: {row['Release_Date']}\nNote: {row['Vote_Average']}/10", axis=1).tolist()
        metadatas = [{"title": t} for t in _df['Title']]
        db = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        db.save_local(FAISS_INDEX_PATH)
        return db

def recherche_semantique(vector_db, requete, k=5):
    docs = vector_db.similarity_search(requete, k=k)
    return [doc.metadata["title"] for doc in docs]
