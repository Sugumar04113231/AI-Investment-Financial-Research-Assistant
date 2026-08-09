def calculate_cagr(initial_value, final_value, years):
    if initial_value <= 0 or years <= 0:
        raise ValueError("Initial value and years must be greater than zero.")
    return round(((final_value / initial_value) ** (1 / years) - 1) * 100, 2)

def calculate_roi(initial_investment, final_value):
    if initial_investment == 0:
        raise ValueError("Initial investment cannot be zero.")
    return round(((final_value - initial_investment) / initial_investment) * 100, 2)

def calculate_growth(old_value, new_value):
    if old_value == 0:
        raise ValueError("Previous value cannot be zero.")
    return round(((new_value - old_value) / abs(old_value)) * 100, 2)

def calculate_profit_margin(revenue, profit):
    if revenue == 0:
        raise ValueError("Revenue cannot be zero.")
    return round((profit / revenue) * 100, 2)

def create_comparison_table(companies):
    if not companies:
        return "No companies provided."
    headers = list(companies[0].keys())
    rows = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    rows += [
        "| " + " | ".join(str(c.get(h, "")) for h in headers) + " |"
        for c in companies
    ]
    return "\n".join(rows)
