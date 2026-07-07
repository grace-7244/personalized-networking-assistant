# app/services/fact_checker.py

import requests
from app.config import settings

WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/w/api.php"


def _search_wikipedia(query: str) -> list:
    """Search Wikipedia and return list of matching page titles."""
    try:
        params = {
            "action": "opensearch",
            "search": query,
            "limit": 3,
            "namespace": 0,
            "format": "json",
        }
        response = requests.get(
            WIKIPEDIA_SEARCH_URL,
            params=params,
            timeout=10,
            headers={"User-Agent": "PersonalizedNetworkingAssistant/1.0"}
        )
        response.raise_for_status()
        data = response.json()
        return data[1] if len(data) > 1 else []
    except Exception:
        return []


def _get_page_summary(title: str) -> str | None:
    """Get summary for a specific Wikipedia page title."""
    try:
        url = WIKIPEDIA_API_URL + requests.utils.quote(title)
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "PersonalizedNetworkingAssistant/1.0"}
        )
        response.raise_for_status()
        data = response.json()

        if data.get("type") == "disambiguation":
            return None

        extract = data.get("extract", "").strip()
        if extract and len(extract) > 50:
            # Return first 3 sentences
            sentences = [s.strip() for s in extract.split(". ") if s.strip()]
            return ". ".join(sentences[:3]) + "."
        return None
    except Exception:
        return None


def fact_check(query: str) -> str:
    """
    Accept a query string and return a summarized fact-check result
    from the Wikipedia REST API using requests.
    """
    if not query or not query.strip():
        return "No query provided, so no fact check could be performed."

    query = query.strip()
    words = query.split()
    meaningful_words = [w for w in words if len(w) > 4]

    # Step 1: Search Wikipedia for the query
    search_results = _search_wikipedia(query)

    if search_results:
        for title in search_results:
            summary = _get_page_summary(title)
            if summary:
                if title.lower() != query.lower():
                    return f"Here is what Wikipedia says about '{title}':\n\n{summary}"
                return summary

    # Step 2: Try each meaningful keyword
    for word in meaningful_words:
        search_results = _search_wikipedia(word)
        if search_results:
            summary = _get_page_summary(search_results[0])
            if summary:
                return f"Here is what Wikipedia says about '{search_results[0]}':\n\n{summary}"

    return (
        f'No Wikipedia article could be found for "{query}". '
        f"Please try a more specific search term."
    )


def get_page_url(query: str) -> str | None:
    """Return the Wikipedia URL for a given query, or None if not found."""
    if not query or not query.strip():
        return None
    try:
        search_results = _search_wikipedia(query.strip())
        if search_results:
            title = requests.utils.quote(search_results[0].replace(" ", "_"))
            return f"https://en.wikipedia.org/wiki/{title}"
        return None
    except Exception:
        return None