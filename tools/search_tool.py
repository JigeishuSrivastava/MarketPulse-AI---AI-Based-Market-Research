from duckduckgo_search import DDGS

def search_web(query):
    # Check if query is valid and not just whitespace
    if not query or not str(query).strip():
        print("Warning: Empty query passed to search_web")
        return []

    links = []
    try:
        with DDGS() as ddgs:
            # Explicitly passing keywords
            results = ddgs.text(keywords=query, max_results=5)
            for r in results:
                links.append(r["href"])
    except Exception as e:
        print(f"Search failed for '{query}': {e}")
        return []
        
    return links