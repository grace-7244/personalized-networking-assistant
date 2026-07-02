# tests/test_routes.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/")
    assert response.status_code == 200
    # main.py returns {"message": "Welcome to the Networking Assistant API!"}
    assert response.json()["message"] == "Welcome to the Networking Assistant API!"


def test_analyze_event() -> None:
    response = client.post(
        "/analyze-event",
        json={"description": "AI for Sustainable Cities"}
    )
    assert response.status_code == 200
    # conversation.py returns {"themes": themes}
    assert "themes" in response.json()
    assert isinstance(response.json()["themes"], list)


def test_generate_conversation() -> None:
    response = client.post(
        "/generate-conversation",
        json={
            "description": "AI for Sustainable Cities",
            "interests": ["climate change", "urban planning"],
        },
    )
    body = response.json()
    assert response.status_code == 200
    # conversation.py returns ConversationResponse: {topics: List[str], suggestions: List[str]}
    assert "topics" in body
    assert "suggestions" in body
    assert isinstance(body["topics"], list)
    assert len(body["suggestions"]) >= 2


def test_fact_check() -> None:
    response = client.post(
        "/fact-check",
        json={"query": "blockchain in healthcare"}
    )
    assert response.status_code == 200
    # conversation.py returns FactCheckResponse: {summary: str}
    assert "summary" in response.json()
    assert isinstance(response.json()["summary"], str)
    assert len(response.json()["summary"]) > 0