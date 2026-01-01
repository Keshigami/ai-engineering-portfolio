import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

def run_rag_pipeline(query, docs_dir="./docs"):
    # 1. Load Documents
    loaders = [PyPDFLoader(os.path.join(docs_dir, f)) for f in os.listdir(docs_dir) if f.endswith('.pdf')]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    
    if not docs:
         # Mock response if no docs found for demo
         return {
             "result": "To request a leave of absence, you must submit a form 30 days in advance to HR.",
             "source_documents": [{"metadata": {"source": "hr_policy.pdf", "page": 2}}]
         }

    # 2. Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    # 3. Embed & Store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    # 4. Retrieval & Q&A
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    result = qa_chain({"query": query})
    return result

if __name__ == "__main__":
    # Example usage
    question = "What is the process for submitting a business expense?"
    # result = run_rag_pipeline(question)
    # print(f"Answer: {result['result']}")
    print("RAG Pipeline script ready. Add PDFs to ./docs to test.")
