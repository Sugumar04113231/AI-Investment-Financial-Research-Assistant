import os

import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agents.news_agent import news_agent
from agents.research_agent import research_company
from agents.pdf_agent import analyze_pdf
from agents.comparison_agent import compare_companies
from agents.report_agent import generate_report
from agents.email_agent import email_report

from rag.pdf_loader import load_pdf
from rag.vectorstore import add_documents

from memory.sqlite_memory import (
    initialize_database, save_message, get_history, clear_history
)
from memory.user_profile import (
    initialize_profile_table, save_profile, get_profile
)

from tools.financial_tool import (
    calculate_cagr, calculate_roi, calculate_growth, calculate_profit_margin
)
from workflows.routing import route_query

load_dotenv()

st.set_page_config(
    page_title="AlphaVest AI Investment Assistant",
    page_icon="📈",
    layout="wide"
)

DATA_DIR = Path("data")
REPORT_DIR = DATA_DIR / "reports"
GENERATED_DIR = Path("generated_reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

initialize_database()
initialize_profile_table()

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "last_pdf_chunks" not in st.session_state:
    st.session_state.last_pdf_chunks = []


def report_to_markdown(report):
    sections = [
        ("Company Overview", report.company_overview),
        ("Industry", report.industry),
        ("Business Model", report.business_model),
    ]
    text = "# Investment Research Report\n\n"
    for title, value in sections:
        text += f"## {title}\n\n{value}\n\n"

    list_sections = [
        ("Latest News", report.latest_news),
        ("Strengths", report.strengths),
        ("Weaknesses", report.weaknesses),
        ("Financial Highlights", report.financial_highlights),
        ("Growth Opportunities", report.growth_opportunities),
        ("Potential Risks", report.potential_risks),
    ]
    for title, values in list_sections:
        text += f"## {title}\n\n"
        for value in values:
            text += f"- {value}\n"
        text += "\n"

    text += f"## Investment Summary\n\n{report.investment_summary}\n\n"
    text += f"---\n\n### Disclaimer\n\n{report.disclaimer}\n"
    return text


def create_pdf(text, filename="investment_report.pdf"):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    path = GENERATED_DIR / filename
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 7))
            continue
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line.startswith("### "):
            story.append(Paragraph(safe[4:], styles["Heading3"]))
        elif line.startswith("## "):
            story.append(Paragraph(safe[3:], styles["Heading2"]))
        elif line.startswith("# "):
            story.append(Paragraph(safe[2:], styles["Title"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + safe[2:], styles["BodyText"]))
        else:
            story.append(Paragraph(safe, styles["BodyText"]))

    doc.build(story)
    return path


def process_query(query):
    q = query.lower().strip()

    # Explicit calculator patterns
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", query)]
    try:
        if "cagr" in q and len(nums) >= 3:
            return f"Calculated CAGR: **{calculate_cagr(nums[0], nums[1], nums[2])}%**", None
        if "roi" in q and len(nums) >= 2:
            return f"Calculated ROI: **{calculate_roi(nums[0], nums[1])}%**", None
        if "growth" in q and len(nums) >= 2:
            return f"Annual Growth: **{calculate_growth(nums[0], nums[1])}%**", None
        if "profit margin" in q and len(nums) >= 2:
            return f"Profit Margin: **{calculate_profit_margin(nums[0], nums[1])}%**", None
    except Exception as exc:
        return f"Calculation error: `{exc}`", None

    try:
        result = route_query(query)
        if isinstance(result, dict):
            if "answer" in result:
                st.session_state.last_pdf_chunks = result.get("chunks", [])
                return result["answer"], result.get("chunks", [])
            if "comparison" in result:
                return result["comparison"], result.get("research", {})
            if "analysis" in result:
                return result["analysis"], result.get("sources", [])
            if "research" in result:
                return result["research"], result.get("web_results", [])
        return str(result), None
    except Exception as exc:
        return (
            "I could not complete that request. "
            f"Please check your API keys/search connection.\n\n`{exc}`",
            None,
        )


# Sidebar
with st.sidebar:
    st.title("📈 AlphaVest AI")
    st.caption("Investment & Financial Research Assistant")

    st.divider()
    st.subheader("👤 Investor Profile")
    profile = get_profile(st.session_state.user_id)

    name = st.text_input("Client Name", value=(profile or {}).get("client_name", ""))
    risk = st.selectbox(
        "Risk Profile",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index((profile or {}).get("risk_profile", "Moderate"))
    )
    industries = st.text_input(
        "Preferred Industries",
        value=(profile or {}).get("preferred_industries", "")
    )
    interests = st.text_input(
        "Investment Interests",
        value=(profile or {}).get("investment_interests", "")
    )
    frequent = st.text_input(
        "Frequently Researched Companies",
        value=(profile or {}).get("frequent_companies", "")
    )

    if st.button("💾 Save Investor Profile", use_container_width=True):
        save_profile(
            st.session_state.user_id, name, risk, industries, interests, frequent
        )
        st.success("Investor profile saved.")

    st.divider()
    st.subheader("📄 Reports / RAG")
    uploads = st.file_uploader(
        "Upload Annual / Quarterly Reports",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploads:
        for uploaded in uploads:
            (REPORT_DIR / uploaded.name).write_bytes(uploaded.getvalue())
        st.success(f"{len(uploads)} PDF(s) uploaded.")

    if st.button("🧠 Build Knowledge Base", use_container_width=True):
        pdfs = list(REPORT_DIR.glob("*.pdf"))
        if not pdfs:
            st.warning("Upload a PDF first.")
        else:
            total = 0
            progress = st.progress(0)
            for i, pdf in enumerate(pdfs):
                chunks = load_pdf(str(pdf))
                total += add_documents(chunks)
                progress.progress((i + 1) / len(pdfs))
            st.success(f"Knowledge base updated: {total} chunks indexed.")

    with st.expander("📚 Uploaded Reports"):
        pdfs = list(REPORT_DIR.glob("*.pdf"))
        if pdfs:
            for pdf in pdfs:
                st.write(f"📄 {pdf.name}")
        else:
            st.write("No reports uploaded.")

    with st.expander("💬 Previous Conversations"):
        history = get_history(st.session_state.user_id)
        if history:
            for role, message, created in history:
                st.markdown(f"**{role}:** {message[:250]}")
        else:
            st.write("No previous conversations.")

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        clear_history(st.session_state.user_id)
        st.rerun()

    st.divider()
    st.subheader("📧 Gmail")
    recipient = st.text_input("Client Email")
    if st.button("Send Latest Report", use_container_width=True):
        if not st.session_state.last_report:
            st.warning("Generate a report first.")
        elif not recipient:
            st.warning("Enter a client email.")
        else:
            try:
                report = st.session_state.last_report
                result = email_report(
                    recipient,
                    report.company,
                    report_to_markdown(report),
                )
                st.success(result)
            except Exception as exc:
                st.error(str(exc))


# Main UI
st.title("📈 AI Investment & Financial Research Assistant")
st.caption("Research • News • RAG • Parallel Comparison • Memory • Reports")
st.info("Educational research tool only — not financial advice.")

st.subheader("Quick Actions")
c1, c2, c3, c4 = st.columns(4)
quick = None
with c1:
    if st.button("🔎 NVIDIA News"):
        quick = "Latest NVIDIA financial news"
with c2:
    if st.button("🏢 Research Microsoft"):
        quick = "Research Microsoft"
with c3:
    if st.button("⚖️ Compare Companies"):
        quick = "Compare Microsoft, Google, Amazon and Meta"
with c4:
    if st.button("📄 Report RAG"):
        quick = "Summarize the uploaded annual report risk factors"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask about companies, reports, markets or calculations...")
if not query:
    query = quick

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    save_message(st.session_state.user_id, "user", query)

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            answer, _ = process_query(query)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_message(st.session_state.user_id, "assistant", answer)

st.divider()
st.subheader("📑 Structured Investment Report")

report_company = st.text_input("Company for report", placeholder="Example: NVIDIA")
if st.button("Generate Investment Report", type="primary"):
    if not report_company:
        st.warning("Enter a company name.")
    else:
        try:
            with st.spinner("Researching and generating structured report..."):
                research = research_company(report_company)
                news = news_agent(report_company)
                report = generate_report(
                    report_company,
                    research["research"],
                    news["analysis"],
                )
                st.session_state.last_report = report

            report_text = report_to_markdown(report)
            st.markdown(report_text)

            safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", report_company)
            txt_path = GENERATED_DIR / f"{safe_name}_report.txt"
            txt_path.write_text(report_text, encoding="utf-8")
            pdf_path = create_pdf(report_text, f"{safe_name}_report.pdf")

            d1, d2 = st.columns(2)
            with d1:
                st.download_button(
                    "⬇️ Download TXT",
                    report_text,
                    file_name=txt_path.name,
                    mime="text/plain",
                )
            with d2:
                st.download_button(
                    "⬇️ Download PDF",
                    pdf_path.read_bytes(),
                    file_name=pdf_path.name,
                    mime="application/pdf",
                )
        except Exception as exc:
            st.error(f"Report generation failed: {exc}")

st.divider()
st.subheader("🧮 Financial Calculator")
calc = st.selectbox("Calculation", ["CAGR", "ROI", "Annual Growth", "Profit Margin"])

if calc == "CAGR":
    a, b, c = st.columns(3)
    initial = a.number_input("Initial Value", min_value=0.01, value=100000.0)
    final = b.number_input("Final Value", min_value=0.01, value=180000.0)
    years = c.number_input("Years", min_value=0.1, value=5.0)
    if st.button("Calculate CAGR"):
        st.success(f"CAGR = {calculate_cagr(initial, final, years)}%")
elif calc == "ROI":
    initial = st.number_input("Initial Investment", min_value=0.01, value=100000.0)
    final = st.number_input("Final Value", min_value=0.01, value=150000.0)
    if st.button("Calculate ROI"):
        st.success(f"ROI = {calculate_roi(initial, final)}%")
elif calc == "Annual Growth":
    old = st.number_input("Previous Value", value=100.0)
    new = st.number_input("Current Value", value=120.0)
    if st.button("Calculate Growth"):
        st.success(f"Growth = {calculate_growth(old, new)}%")
else:
    revenue = st.number_input("Revenue", min_value=0.01, value=100000.0)
    profit = st.number_input("Profit", value=15000.0)
    if st.button("Calculate Margin"):
        st.success(f"Profit Margin = {calculate_profit_margin(revenue, profit)}%")

if st.session_state.last_pdf_chunks:
    with st.expander("📄 Retrieved PDF Chunks"):
        for i, chunk in enumerate(st.session_state.last_pdf_chunks, 1):
            st.markdown(f"### Chunk {i}")
            st.caption(
                f"Source: {chunk.metadata.get('source', 'Unknown')} | "
                f"Page: {chunk.metadata.get('page', 'Unknown')}"
            )
            st.write(chunk.page_content)
