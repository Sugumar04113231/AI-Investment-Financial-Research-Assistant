from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from agents.research_agent import research_company
from agents.coordinator import get_llm

def normalize_company_names(companies):
    cleaned = []
    for company in companies:
        company = company.strip().strip(".")
        if company and company.lower() not in [x.lower() for x in cleaned]:
            cleaned.append(company)
    return cleaned

def compare_companies(companies):
    companies = normalize_company_names(companies)
    if len(companies) < 2:
        raise ValueError("At least two companies are required.")

    parallel = RunnableParallel({
        company: (lambda x, c=company: research_company(c))
        for company in companies
    })
    results = parallel.invoke({"companies": companies})

    combined = "\n\n".join(
        f"COMPANY: {company}\n{result['research']}"
        for company, result in results.items()
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior investment research analyst.
Compare the supplied companies based only on the supplied research.
Discuss business model, products, growth, strengths, weaknesses and risks.
Do not invent financial values. End with a balanced research conclusion."""),
        ("human", "Companies: {companies}\n\nResearch:\n{research}"),
    ])
    response = (prompt | get_llm()).invoke({
        "companies": ", ".join(companies),
        "research": combined,
    })
    return {
        "companies": companies,
        "research": results,
        "comparison": response.content,
    }
