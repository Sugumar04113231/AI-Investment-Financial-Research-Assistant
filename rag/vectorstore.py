import os
import uuid
from langchain_chroma import Chroma
from rag.embeddings import get_embeddings

def get_vectorstore():
    return Chroma(
        collection_name=os.getenv("CHROMA_COLLECTION", "financial_reports"),
        embedding_function=get_embeddings(),
        persist_directory=os.getenv("CHROMA_PATH", "data/chroma"),
    )

def add_documents(documents):
    if not documents:
        return 0
    ids = [str(uuid.uuid4()) for _ in documents]
    get_vectorstore().add_documents(documents=documents, ids=ids)
    return len(documents)

def get_retriever():
    return get_vectorstore().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )
