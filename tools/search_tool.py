from ddgs import DDGS

def search_web(query: str, max_results: int = 8):
    results = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                })
    except Exception as exc:
        results.append({"title": "Search Error", "url": "", "snippet": str(exc)})
    return results

def format_search_results(results):
    if not results:
        return "No search results found."
    return "\n\n".join(
        f"SOURCE {i}\nTitle: {r['title']}\nURL: {r['url']}\nSummary: {r['snippet']}"
        for i, r in enumerate(results, 1)
    )
