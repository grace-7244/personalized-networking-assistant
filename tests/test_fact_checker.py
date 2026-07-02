"""
test_fact_checker.py

Unit tests for app/services/fact_checker.py.

These tests mock the `wikipedia` package directly so they run fast,
deterministically, and without needing network access.
"""

import pytest
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException

from app.services import fact_checker


# ---------------------------------------------------------------------
# fact_check() — happy path
# ---------------------------------------------------------------------

def test_fact_check_returns_summary(monkeypatch):
    """A normal query should return the stripped summary text."""

    def fake_summary(query, sentences, auto_suggest, redirect):
        return "  Python is a high-level programming language.  "

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("Python programming language")

    assert result == "Python is a high-level programming language."


def test_fact_check_strips_whitespace_from_query(monkeypatch):
    """Leading/trailing whitespace in the query itself shouldn't break lookup."""
    captured = {}

    def fake_summary(query, sentences, auto_suggest, redirect):
        captured["query"] = query
        return "Some summary."

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    fact_checker.fact_check("   Ada Lovelace   ")

    assert captured["query"] == "Ada Lovelace"


# ---------------------------------------------------------------------
# fact_check() — empty / invalid input
# ---------------------------------------------------------------------

@pytest.mark.parametrize("query", ["", "   ", None])
def test_fact_check_handles_empty_query(query):
    result = fact_checker.fact_check(query)
    assert result == "No query provided, so no fact check could be performed."


# ---------------------------------------------------------------------
# fact_check() — PageError (no article found)
# ---------------------------------------------------------------------

def test_fact_check_handles_page_error(monkeypatch):
    def fake_summary(query, sentences, auto_suggest, redirect):
        raise PageError(query)

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("asdkjqwlekjasldkj")

    assert "No Wikipedia article was found" in result
    assert "asdkjqwlekjasldkj" in result


# ---------------------------------------------------------------------
# fact_check() — DisambiguationError
# ---------------------------------------------------------------------

def test_fact_check_resolves_disambiguation_with_first_valid_option(monkeypatch):
    """
    If the first query is ambiguous, fact_check should try the
    suggested options and return the first one that resolves.
    """

    def fake_summary(query, sentences, auto_suggest, redirect):
        if query == "Mercury":
            raise DisambiguationError("Mercury", ["Mercury (planet)", "Mercury (element)"])
        if query == "Mercury (planet)":
            return "Mercury is the closest planet to the Sun."
        raise AssertionError(f"Unexpected query: {query}")

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("Mercury")

    assert result == "Mercury is the closest planet to the Sun."


def test_fact_check_disambiguation_all_options_fail(monkeypatch):
    """
    If none of the disambiguation options resolve, return a
    human-readable ambiguity message instead of raising.
    """

    def fake_summary(query, sentences, auto_suggest, redirect):
        if query == "Java":
            raise DisambiguationError("Java", ["Java (island)", "Java (programming language)"])
        raise WikipediaException("still ambiguous")

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("Java")

    assert "ambiguous" in result.lower()
    assert "Java" in result


# ---------------------------------------------------------------------
# fact_check() — generic Wikipedia/network errors
# ---------------------------------------------------------------------

def test_fact_check_handles_wikipedia_exception(monkeypatch):
    def fake_summary(query, sentences, auto_suggest, redirect):
        raise WikipediaException("network timeout")

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("Black holes")

    assert result == "Fact check is temporarily unavailable. Please try again shortly."


def test_fact_check_handles_unexpected_exception(monkeypatch):
    def fake_summary(query, sentences, auto_suggest, redirect):
        raise RuntimeError("something totally unexpected")

    monkeypatch.setattr(fact_checker.wikipedia, "summary", fake_summary)

    result = fact_checker.fact_check("quantum computing")

    assert result == "An unexpected error occurred while fact-checking this topic."


# ---------------------------------------------------------------------
# get_page_url()
# ---------------------------------------------------------------------

def test_get_page_url_returns_url(monkeypatch):
    class FakePage:
        url = "https://en.wikipedia.org/wiki/Ada_Lovelace"

    def fake_page(query, auto_suggest, redirect):
        return FakePage()

    monkeypatch.setattr(fact_checker.wikipedia, "page", fake_page)

    result = fact_checker.get_page_url("Ada Lovelace")

    assert result == "https://en.wikipedia.org/wiki/Ada_Lovelace"


def test_get_page_url_returns_none_on_error(monkeypatch):
    def fake_page(query, auto_suggest, redirect):
        raise PageError(query)

    monkeypatch.setattr(fact_checker.wikipedia, "page", fake_page)

    result = fact_checker.get_page_url("nonexistent topic xyz")

    assert result is None


def test_get_page_url_handles_empty_query():
    assert fact_checker.get_page_url("") is None
    assert fact_checker.get_page_url(None) is None