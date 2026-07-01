# app/routers/conversation.py

from fastapi import APIRouter
from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    FactCheckRequest,
    FactCheckResponse,
    EventInput,
)
from app.services.event_analyzer import analyze_event
from app.services.topic_generator import generate_conversation
from app.services.fact_checker import fact_check

router = APIRouter()


@router.post("/analyze-event", summary="Analyze Event")
def analyze_event_route(event: EventInput):
    """
    Accepts an event description and returns extracted themes
    using DistilBERT zero-shot classification.
    """
    themes = analyze_event(event.description)
    return {"themes": themes}


@router.post("/fact-check", response_model=FactCheckResponse, summary="Fact Check")
def fact_check_route(request: FactCheckRequest):
    """
    Accepts a query string and returns a summarized fact-check
    result retrieved from the Wikipedia API.
    """
    summary = fact_check(request.query)
    return FactCheckResponse(summary=summary)


@router.post("/generate-conversation", response_model=ConversationResponse, summary="Generate Conversation")
def generate_conversation_route(request: ConversationRequest):
    """
    Accepts an event description and user interests, extracts themes
    using DistilBERT, and generates conversation starters using GPT-2.
    """
    themes = analyze_event(request.description)
    suggestions = generate_conversation(request.description, request.interests)
    return ConversationResponse(topics=themes, suggestions=suggestions)