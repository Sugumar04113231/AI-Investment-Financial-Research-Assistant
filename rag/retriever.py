from rag.vectorstore import get_retriever

def retrieve_documents(question):
    return get_retriever().invoke(question)

def format_documents(documents):
    if not documents:
        return "No relevant document chunks found."
    return "\n\n".join(
        f"CHUNK {i}\nSource: {doc.metadata.get('source', 'Unknown')}\n"
        f"Page: {doc.metadata.get('page', 'Unknown')}\nContent:\n{doc.page_content}"
        for i, doc in enumerate(documents, 1)
    )
