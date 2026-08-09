from agents.research_agent import research_company
from agents.news_agent import news_agent
from agents.report_agent import generate_report

def sequential_research_workflow(company):
    research = research_company(company)
    news = news_agent(company)
    report = generate_report(
        company,
        research["research"],
        news["analysis"],
    )
    return {"research": research, "news": news, "report": report}
