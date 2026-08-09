import wikipedia

def search_wikipedia(company: str):
    try:
        results = wikipedia.search(company)
        if not results:
            return "No Wikipedia information found."
        page = wikipedia.page(results[0], auto_suggest=False)
        return page.summary[:10000]
    except Exception as exc:
        return f"Wikipedia error: {exc}"
