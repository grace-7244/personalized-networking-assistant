# Centralized Routing Architecture — Personalized Networking Assistant

## Overview

The routing architecture in this application follows a **hub-and-spoke model** where `main.py` acts as the central hub that assembles the application from modular router components.

This design pattern is especially important as applications grow — it allows new feature areas (such as a future `/users` or `/recommendations` endpoint) to be added as separate router files **without touching any existing code**.

---

## Hub-and-Spoke Model

```
                    ┌─────────────┐
                    │   main.py   │  ← Central Hub
                    │  (FastAPI)  │
                    └──────┬──────┘
                           │ include_router()
                           │
              ┌────────────▼────────────┐
              │  routers/conversation.py │  ← Spoke
              │                          │
              │  POST /analyze-event     │
              │  POST /fact-check        │
              │  POST /generate-conv...  │
              │  GET  /                  │
              └──────────────────────────┘

         Future spokes (just add new router files):
              routers/users.py         → /users
              routers/recommendations.py → /recommendations
```

---

## API Endpoints

All routes are visible in the auto-generated **Swagger UI** at `http://localhost:8000/docs`:

| Method | Endpoint | Summary | Description |
|---|---|---|---|
| `POST` | `/analyze-event` | Analyze Event | Accepts an event description and returns themes extracted by DistilBERT |
| `POST` | `/fact-check` | Fact Check | Accepts a query and returns a Wikipedia-sourced fact-check summary |
| `POST` | `/generate-conversation` | Generate Conversation | Accepts event description + interests and returns AI-generated conversation starters |
| `GET` | `/` | Root | Health-check endpoint confirming the API is running |

---

## Router Code

All routes are defined in `app/routers/conversation.py`:

```python
# app/routers/conversation.py

from fastapi import APIRouter
from app.models.schemas import (
    ConversationRequest, ConversationResponse,
    FactCheckRequest, FactCheckResponse, EventInput,
)
from app.services.event_analyzer import analyze_event
from app.services.topic_generator import generate_conversation
from app.services.fact_checker import fact_check

router = APIRouter()

@router.post("/analyze-event", summary="Analyze Event")
def analyze_event_route(event: EventInput):
    themes = analyze_event(event.description)
    return {"themes": themes}

@router.post("/fact-check", response_model=FactCheckResponse, summary="Fact Check")
def fact_check_route(request: FactCheckRequest):
    summary = fact_check(request.query)
    return FactCheckResponse(summary=summary)

@router.post("/generate-conversation", response_model=ConversationResponse, summary="Generate Conversation")
def generate_conversation_route(request: ConversationRequest):
    themes = analyze_event(request.description)
    suggestions = generate_conversation(request.description, request.interests)
    return ConversationResponse(topics=themes, suggestions=suggestions)
```

---

## Understanding the Request Lifecycle

How a request flows through the system from the moment the Streamlit frontend sends an HTTP POST to when the user sees a result:

```
Step 1: User clicks "Generate Starters" in Streamlit
        ↓
Step 2: Streamlit sends POST /generate-conversation
        with JSON body: { "description": "...", "interests": [...] }
        ↓
Step 3: FastAPI receives the request at main.py
        ↓
Step 4: main.py routes it to conversation.router
        (registered via app.include_router)
        ↓
Step 5: conversation.py validates the request body
        against ConversationRequest (Pydantic model)
        → If invalid: FastAPI returns 422 automatically
        → If valid: continues to step 6
        ↓
Step 6: Route handler calls the service layer:
        → analyze_event(description)   [DistilBERT]
        → generate_conversation(...)   [GPT-2]
        ↓
Step 7: Services return results to the route handler
        ↓
Step 8: Route handler builds a ConversationResponse object
        and FastAPI serializes it to JSON automatically
        ↓
Step 9: Streamlit receives the JSON response
        and displays the conversation starters to the user
```

---

## Why This Architecture?

| Benefit | Explanation |
|---|---|
| **Separation of concerns** | Routes handle HTTP only — no business logic inside route handlers |
| **Easy to extend** | Add a new `routers/users.py` and one `include_router()` line in `main.py` |
| **No code breakage** | Adding new routes never touches existing route files |
| **Auto-documentation** | Swagger UI at `/docs` is generated automatically from route definitions |
| **Auto-validation** | Pydantic models validate every request — no manual checks needed |

---

## File Structure for Routing

```
app/
├── main.py                    ← Hub: creates app, registers routers
└── routers/
    └── conversation.py        ← Spoke: defines all conversation-related routes
```