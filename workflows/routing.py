from langchain_core.runnables import RunnableBranch, RunnableLambda
from agents.news_agent import news_agent
from agents.pdf_agent import analyze_pdf
from agents.comparison_agent import compare_companies
from agents.research_agent import research_company

def classify_query(query):
    q = query.lower()
    if any(x in q for x in ["compare", "comparison", " vs ", " versus "]):
        return "comparison"
    if any(x in q for x in [
        "annual report", "quarterly report", "uploaded report",
        "pdf", "risk factors", "future plans", "revenue growth"
    ]):
        return "pdf"
    if any(x in q for x in [
        "latest news", "financial news", "earnings",
        "stock news", "market news", "industry news"
    ]):
        return "news"
    return "research"

def extract_companies(query):
    text = query
    for word in ["compare", "comparison", "companies", "between"]:
        text = text.replace(word, "")
    parts = text.replace(" versus ", ",").replace(" vs ", ",").replace(" and ", ",").split(",")
    companies = [p.strip() for p in parts if p.strip()]
    return companies

def route_query(query):
    route = classify_query(query)

    branch = RunnableBranch(
        (
            lambda x: x["route"] == "news",
            RunnableLambda(lambda x: news_agent(x["query"]))
        ),
        (
            lambda x: x["route"] == "pdf",
            RunnableLambda(lambda x: analyze_pdf(x["query"]))
        ),
        (
            lambda x: x["route"] == "comparison",
            RunnableLambda(lambda x: compare_companies(extract_companies(x["query"])))
        ),
        RunnableLambda(lambda x: research_company(x["query"]))
    )
    return branch.invoke({"route": route, "query": query})
