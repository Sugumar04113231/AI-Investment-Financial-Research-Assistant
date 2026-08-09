from langchain_core.prompts import ChatPromptTemplate
from agents.coordinator import get_llm
from tools.search_tool import search_web, format_search_results

def news_agent(topic: str):
    results = search_web(
        f"{topic} latest financial news earnings stock announcements",
        max_results=8,
    )
    context = format_search_results(results)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a financial news research analyst.
Use only the supplied search results. Focus on recent announcements,
earnings, market developments, partnerships, products and regulatory events.
Do not invent facts. Mention that search information can be time-sensitive."""),
        ("human", "Topic: {topic}\n\nSearch Results:\n{context}"),
    ])
    response = (prompt | get_llm()).invoke({"topic": topic, "context": context})
    return {"topic": topic, "sources": results, "analysis": response.content}
