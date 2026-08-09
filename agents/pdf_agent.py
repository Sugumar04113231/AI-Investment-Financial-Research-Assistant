from langchain_core.prompts import ChatPromptTemplate
from agents.coordinator import get_llm
from rag.retriever import retrieve_documents, format_documents

def analyze_pdf(question: str):
    docs = retrieve_documents(question)
    context = format_documents(docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an annual-report analyst.
Answer ONLY from the retrieved document context.
If the answer is not present, say so. Include page/source information
when available."""),
        ("human", "Question: {question}\n\nRetrieved Context:\n{context}"),
    ])
    response = (prompt | get_llm()).invoke(
        {"question": question, "context": context}
    )
    return {"answer": response.content, "chunks": docs}
