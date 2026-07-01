# Application Architecture — Personalized Networking Assistant

This document describes the system architecture of the Personalized Networking Assistant, including the architectural overview, directory structure, and module design principles.

---

## Architectural Overview

With models selected, the next step was defining a clean, modular system architecture. The architecture was designed to support:

- **Separation of concerns** — frontend, backend, and AI services can be developed and maintained independently
- **Easy testability** — each service module is independently testable with no tight coupling
- **Extensibility** — new features like authentication or database integration can be added with minimal disruption to existing code

The application follows a **three-tier architecture** with a clear data flow from the user interface through the API layer down to the AI service modules.

```
┌─────────────────────────────────────┐
│        User Interface (Streamlit)   │  ← Tier 1: Frontend
└────────────────┬────────────────────┘
                 │ HTTPS / JSON
┌────────────────▼────────────────────┐
│       API Layer (FastAPI)           │  ← Tier 2: Backend
│   Routes → Orchestration Handler   │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│    AI & NLP Services (Local)        │  ← Tier 3: AI/Service Layer
│  DistilBERT │ GPT-2 │ Wikipedia API │
└─────────────────────────────────────┘
```

---

## Directory Structure and Module Design

The project is organized into a clean directory hierarchy that separates application code, frontend, tests, and configuration. This structure keeps the codebase navigable and ensures that adding new features requires minimal disruption to existing code.

```
personalized-networking-assistant/
│
├── app/                          # Core backend application
│   ├── models/
│   │   └── schemas.py            # Pydantic data models & request/response schemas
│   │
│   ├── routers/
│   │   └── conversation.py       # FastAPI route definitions
│   │
│   ├── services/
│   │   ├── event_analyzer.py     # DistilBERT theme extraction service
│   │   ├── fact_checker.py       # Wikipedia API fact verification service
│   │   ├── feedback_logger.py    # Feedback capture & persistence service
│   │   ├── history_logger.py     # Conversation history persistence service
│   │   └── topic_generator.py    # GPT-2 conversation starter generation service
│   │
│   ├── config.py                 # App-wide configuration & environment settings
│   └── main.py                   # Application entry point — initializes FastAPI app
│
├── tests/                        # All unit and integration tests
│   ├── conftest.py               # Shared pytest fixtures and test configuration
│   ├── test_event_analyzer.py    # Tests for the event analyzer service
│   ├── test_fact_checker.py      # Tests for the fact checker service
│   └── test_routes.py            # Tests for FastAPI API endpoints
│
├── frontend/
│   └── streamlit_app.py          # Streamlit UI application
│
├── data/
│   ├── history.json              # Persisted conversation history
│   └── feedback.json             # Persisted user feedback logs
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview and setup instructions
```

---

## Module Responsibilities

### `app/models/schemas.py`
Defines all Pydantic models used for request validation and response serialization across the FastAPI routes. Ensures data integrity at the API boundary.

### `app/routers/conversation.py`
Contains all FastAPI route definitions (`/generate-conversation`, `/fact-check`, `/analyze-event`). Routes delegate business logic to the service layer — keeping route handlers thin and readable.

### `app/services/`
The core service layer. Each file is a self-contained module responsible for one specific function:

| File | Responsibility |
|---|---|
| `event_analyzer.py` | Runs DistilBERT zero-shot classification to extract themes from event descriptions |
| `topic_generator.py` | Uses GPT-2 text generation to produce context-aware conversation starters |
| `fact_checker.py` | Queries the Wikipedia API and returns a summarized fact-check result |
| `history_logger.py` | Reads and writes conversation history to `history.json` |
| `feedback_logger.py` | Reads and writes user feedback (thumbs up/down) to `feedback.json` |

### `app/config.py`
Centralizes all configuration values such as model names, file paths, and API settings. Any change to configuration happens in one place only.

### `app/main.py`
The application entry point. Initializes the FastAPI app instance, registers all routers, and configures middleware. Running this file starts the backend server.

### `tests/`
All tests are co-located in a dedicated `tests/` folder, completely separate from application code. `conftest.py` provides shared fixtures reused across test files.

---

## Design Principles

| Principle | How It Is Applied |
|---|---|
| Separation of concerns | Frontend, API routes, and AI services are in completely separate modules |
| Single responsibility | Each service file does exactly one thing |
| Thin controllers | Route handlers only validate input and delegate — no business logic inside routes |
| Local-first persistence | JSON files replace a database, keeping setup simple and portable |
| Independent testability | Every service can be unit-tested in isolation without starting the full app |

---

## Tech Stack Summary

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Interactive web UI |
| Backend | FastAPI | REST API with automatic validation and Swagger docs |
| Theme Extraction | DistilBERT (Hugging Face) | Zero-shot classification of event themes |
| Text Generation | GPT-2 Small (Hugging Face) | Generating conversation starters |
| Fact Verification | Wikipedia API (Python wrapper) | Retrieving factual references |
| Data Persistence | Local JSON files | Storing history and feedback without a database |
| Testing | Pytest + Httpx | Unit tests and API endpoint testing |