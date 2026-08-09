from tools.email_tool import send_email

def email_report(recipient, company, report_text):
    send_email(
        recipient=recipient,
        subject=f"Investment Research Report - {company}",
        body=report_text,
    )
    return f"Investment report successfully emailed to {recipient}."
