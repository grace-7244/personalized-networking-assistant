from app.services.event_analyzer import analyze_event

def test_analyze_event_returns_list_of_strings():
    result = analyze_event("AI for Sustainable Cities")
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(theme, str) for theme in result)

def test_analyze_event_relevant_theme():
    result = analyze_event("A conference about artificial intelligence")
    assert any("intelligence" in theme.lower() or "technology" in theme.lower() for theme in result)