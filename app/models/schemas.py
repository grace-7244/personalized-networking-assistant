# app/models/schemas.py

from pydantic import BaseModel
from typing import List


# -------------------------------------------------------------------
# Input Models
# -------------------------------------------------------------------

class EventInput(BaseModel):
    """Represents a single event description submitted by the user."""
    description: str


class UserInterests(BaseModel):
    """Represents the list of interests provided by the user."""
    interests: List[str]


class ConversationRequest(BaseModel):
    """
    Combined request model for generating conversation starters.
    Sent by the frontend when the user clicks 'Generate Starters'.
    Contains both the event description and the user's interests.
    """
    description: str
    interests: List[str]


# -------------------------------------------------------------------
# Output Models
# -------------------------------------------------------------------

class ConversationResponse(BaseModel):
    """
    Response model returned after generating conversation starters.
    Contains extracted themes and the AI-generated suggestions.
    """
    topics: List[str]
    suggestions: List[str]


class FactCheckRequest(BaseModel):
    """Request model for the fact-checking endpoint."""
    query: str


class FactCheckResponse(BaseModel):
    """
    Response model returned after a Wikipedia fact-check query.
    Contains a summarized result from the Wikipedia API.
    """
    summary: str