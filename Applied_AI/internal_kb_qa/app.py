import streamlit as st
import os
from rag_pipeline import run_rag_pipeline
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Internal KB Q&A", layout="wide")

st.title("📚 Internal Knowledge-Base Q&A")
st.markdown("""
This tool uses RAG (Retrieval-Augmented Generation) to answer questions based on your internal documentation.
**Goal**: Reduce search time by providing instant, cited answers.
""")

with st.sidebar:
    st.header("Settings")
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ OpenAI API Key not found. Running in DEMO mode with mock data.")
    
    st.subheader("Stored Documents")
    docs_dir = "./docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    docs = [f for f in os.listdir(docs_dir) if f.endswith('.pdf')]
    if docs:
        for doc in docs:
            st.text(f"📄 {doc}")
    else:
        st.info("No PDFs found in ./docs. Add some to test real retrieval.")

query = st.text_input("Ask a question about company policy:", placeholder="e.g., How do I request for a leave?")

if st.button("Search"):
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching knowledge base..."):
            result = run_rag_pipeline(query)
            
            st.markdown("### 🤖 Answer")
            st.write(result['result'])
            
            st.markdown("### 📍 Citations")
            for doc in result['source_documents']:
                source = doc['metadata'].get('source', 'Unknown')
                page = doc['metadata'].get('page', '?')
                st.caption(f"Source: {source} (Page {page})")
