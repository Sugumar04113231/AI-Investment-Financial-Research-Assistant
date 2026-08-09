from langchain_core.prompts import ChatPromptTemplate
from agents.coordinator import get_llm
from tools.search_tool import search_web, format_search_results
from tools.wikipedia_tool import search_wikipedia

def research_company(company: str):
    web_results = search_web(
        f"{company} business products competitors revenue sources latest announcements",
        max_results=8,
    )
    web = format_search_results(web_results)
    wiki = search_wikipedia(company)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional equity research analyst.
Prepare a factual company research brief covering business overview,
products, competitors, revenue sources and recent announcements.
Use only supplied information and do not fabricate numbers."""),
        ("human", "Company: {company}\n\nWeb:\n{web}\n\nWikipedia:\n{wiki}"),
    ])
    response = (prompt | get_llm()).invoke(
        {"company": company, "web": web, "wiki": wiki}
    )
    return {
        "company": company,
        "web_results": web_results,
        "wikipedia": wiki,
        "research": response.content,
    }
