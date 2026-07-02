# app/services/fact_checker.py

"""
fact_checker.py
Retrieves and summarizes factual references from the Wikipedia API.
Uses the wikipedia Python wrapper to search and return article summaries.
"""

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException

from app.config import settings

# Set language from config
wikipedia.set_lang(settings.WIKIPEDIA_LANG)


def fact_check(query: str) -> str:
    """
    Accept a query string and return a summarized fact-check result
    from the Wikipedia API.

    Args:
        query: the topic or claim to look up.

    Returns:
        A plain-text summary string, or a human-readable error message.
    """
    # Handle empty / None queries
    if not query or not query.strip():
        return "No query provided, so no fact check could be performed."

    query = query.strip()

    try:
        summary = wikipedia.summary(
            query,
            sentences=settings.WIKIPEDIA_SUMMARY_SENTENCES,
            auto_suggest=True,
            redirect=True,
        )
        return summary.strip()

    except DisambiguationError as e:
        # Try each suggested option up to the configured limit
        attempts = e.options[:settings.WIKIPEDIA_MAX_DISAMBIGUATION_ATTEMPTS]
        for option in attempts:
            try:
                summary = wikipedia.summary(
                    option,
                    sentences=settings.WIKIPEDIA_SUMMARY_SENTENCES,
                    auto_suggest=False,
                    redirect=True,
                )
                return summary.strip()
            except (WikipediaException, Exception):
                continue
        # All options failed
        return (
            f'"{query}" is ambiguous and could refer to multiple topics. '
            f"Please be more specific."
        )

    except PageError:
        return (
            f'No Wikipedia article was found for "{query}". '
            f"Please try a different search term."
        )

    except WikipediaException:
        return "Fact check is temporarily unavailable. Please try again shortly."

    except Exception:
        return "An unexpected error occurred while fact-checking this topic."


def get_page_url(query: str) -> str | None:
    """
    Return the Wikipedia URL for a given query, or None if not found.

    Args:
        query: the topic to look up.

    Returns:
        URL string or None.
    """
    if not query or not query.strip():
        return None

    try:
        page = wikipedia.page(
            query.strip(),
            auto_suggest=True,
            redirect=True,
        )
        return page.url
    except Exception:
        return None