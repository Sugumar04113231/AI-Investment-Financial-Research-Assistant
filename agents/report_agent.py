from langchain_core.prompts import ChatPromptTemplate
from agents.coordinator import get_llm
from models.investment_report import InvestmentReport

def generate_report(company, research, news="", pdf_context=""):
    structured_llm = get_llm().with_structured_output(InvestmentReport)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior financial research analyst.
Generate a professional, balanced investment research report using only
the supplied information. Never invent financial numbers. The report is
research/education, not guaranteed investment advice."""),
        ("human", """Company: {company}

Company Research:
{research}

Latest News:
{news}

Report Context:
{pdf_context}"""),
    ])
    return (prompt | structured_llm).invoke({
        "company": company,
        "research": research,
        "news": news,
        "pdf_context": pdf_context,
    })
