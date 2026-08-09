from typing import List
from pydantic import BaseModel, Field

class InvestmentReport(BaseModel):
    company: str = Field(description="Company name")
    company_overview: str
    industry: str
    business_model: str
    latest_news: List[str]
    strengths: List[str]
    weaknesses: List[str]
    financial_highlights: List[str]
    growth_opportunities: List[str]
    potential_risks: List[str]
    investment_summary: str
    disclaimer: str = (
        "This report is for educational and research purposes only "
        "and is not financial advice."
    )
