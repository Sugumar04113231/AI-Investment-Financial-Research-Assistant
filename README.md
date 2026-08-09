# 📈 AI Investment & Financial Research Assistant

## AlphaVest Capital Capstone Project 3

A LangChain + Streamlit financial research assistant that combines web research,
financial-news analysis, PDF RAG, multi-company comparison, memory,
financial calculations, structured reports and Gmail delivery.

## Features

- Conversational financial assistant
- Financial news search with DuckDuckGo
- Company research with web search + Wikipedia
- Annual/quarterly report RAG with ChromaDB
- Multi-company research using `RunnableParallel`
- Conditional routing using `RunnableBranch`
- Sequential research workflow
- Pydantic structured investment reports
- CAGR / ROI / Growth / Profit Margin tools
- SQLite conversation memory
- Long-term investor profile memory
- TXT/PDF report downloads
- Gmail report delivery
- Streamlit UI

## Architecture

Investor → Streamlit → Coordinator → News / Research / PDF / Comparison / Email
→ SQLite + ChromaDB → Structured Report

## Installation

### 1. Create environment

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Optional Gmail:

```text
GMAIL_SENDER=...
GMAIL_APP_PASSWORD=...
```

### 4. Run

```bash
streamlit run app.py
```

## PDF RAG

1. Open the Streamlit application.
2. Upload an annual/quarterly report.
3. Click **Build Knowledge Base**.
4. Ask questions such as:
   - Summarize the risk factors.
   - Explain revenue growth.
   - What are the future plans?

## Comparison

Try:

```text
Compare Microsoft, Google, Amazon and Meta
```

The application uses `RunnableParallel` to research the companies in parallel.

## Routing

Examples:

```text
Latest NVIDIA financial news
```
→ News Agent

```text
Research Microsoft
```
→ Research Agent

```text
Analyze the annual report risk factors
```
→ PDF/RAG Agent

```text
Compare Google and Amazon
```
→ Parallel Comparison Agent

## Financial Calculator

The UI supports:

- CAGR
- ROI
- Annual Growth
- Profit Margin

## Structured Report

Generated reports contain:

- Company Overview
- Industry
- Business Model
- Latest News
- Strengths
- Weaknesses
- Financial Highlights
- Growth Opportunities
- Potential Risks
- Investment Summary

## Memory

SQLite stores conversation history and investor profile information such as:

- Client name
- Risk profile
- Preferred industries
- Investment interests
- Frequently researched companies

## Gmail

Use a Google App Password with SMTP. Do not place your normal Gmail password in `.env`.

## Project Structure

```text
AI-Investment-Financial-Research-Assistant/
├── app.py
├── agents/
├── tools/
├── rag/
├── memory/
├── workflows/
├── models/
├── data/
├── generated_reports/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Capstone Requirement Mapping

| Requirement | Implementation |
|---|---|
| Streamlit | `app.py` |
| News Agent | `agents/news_agent.py` |
| Company Research | `agents/research_agent.py` |
| PDF RAG | `rag/` |
| ChromaDB | `rag/vectorstore.py` |
| RunnableParallel | `agents/comparison_agent.py` |
| RunnableBranch | `workflows/routing.py` |
| Sequential Workflow | `workflows/sequential.py` |
| Pydantic | `models/investment_report.py` |
| Python Financial Tool | `tools/financial_tool.py` |
| SQLite Memory | `memory/sqlite_memory.py` |
| Long-term Profile | `memory/user_profile.py` |
| Gmail | `tools/email_tool.py` |
| TXT/PDF Reports | `app.py` |

## Disclaimer

This project is an educational financial research assistant. Generated information
may be incomplete, delayed or inaccurate. It is not financial, investment, tax or
legal advice and should not be used as the sole basis for investment decisions.
