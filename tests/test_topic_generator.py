from app.services.topic_generator import generate_conversation

def test_generate_conversation_returns_list_of_strings():
    result = generate_conversation("AI for Sustainable Cities", ["climate change", "urban planning"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, str) for item in result)

def test_generate_conversation_no_interests():
    result = generate_conversation("Tech networking meetup", [])
    assert isinstance(result, list)
    assert len(result) > 0