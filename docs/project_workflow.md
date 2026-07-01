# Project Workflow — Personalized Networking Assistant

This document outlines the complete project workflow organized into Epics and Stories. Each Epic represents a major phase of development, and each Story within it represents a specific deliverable or implementation task.

---

## Overview

```
Epic 1: Model Selection & Architecture
    └── Research → Architecture → Environment Setup

Epic 2: Core Functionalities Development
    └── Schema → Services (Analyzer, Generator, Fact Checker, Loggers) → API Routes → Entry Point

Epic 3: Main Application Logic
    └── Routing → Service Layer → FastAPI Features

Epic 4: Frontend UI Using Streamlit
    └── Setup → Input → Results → Fact Check → History → Feedback → State Management

Epic 5: Testing & Local Deployment
    └── Philosophy → Unit Tests → API Tests → Run Tests → Deploy → Manual Verify
```

---

## Epic 1: Model Selection and Architecture

**Goal:** Establish the technical foundation — choose the right AI models, define the system architecture, and prepare the development environment.

| Story | Task | Description |
|---|---|---|
| Story 1 | Model Research & Selection | Evaluate and select Hugging Face models. Use DistilBERT for zero-shot theme classification and GPT-2 Small for conversational text generation. |
| Story 2 | Defining the Application Architecture | Design the overall system architecture including the Streamlit frontend, FastAPI backend, AI/NLP service layer, fact verification module, and local data store. |
| Story 3 | Environment Setup | Set up Python 3.11+ virtual environment and install all required dependencies: Streamlit, FastAPI, Hugging Face Transformers, Wikipedia API, Pytest, Httpx, and Git. |

---

## Epic 2: Core Functionalities Development

**Goal:** Build all backend services and API routes that power the core features of the application.

| Story | Task | Description |
|---|---|---|
| Story 1 | Data Schema Definition | Define the data structures and JSON schemas used across all services, aligned with the ER diagram entities. |
| Story 2 | Event Analyzer Service | Build `event_analyzer.py` using DistilBERT zero-shot classification to extract themes from event descriptions. |
| Story 3 | Topic Generator Service | Build `topic_generator.py` using GPT-2 text generation pipeline to produce context-aware conversation starters. |
| Story 4 | Fact Checker Service | Build `fact_checker.py` using the Wikipedia Python API wrapper to retrieve and summarize factual references. |
| Story 5 | History Logger Service | Build the history logger to save all generated conversations to `history.json` for future review. |
| Story 6 | Feedback Logger Service | Build the feedback logger to capture user thumbs up/down actions and save them to `feedback.json`. |
| Story 7 | API Routes Implementation | Define and implement FastAPI routes: `/generate-conversation`, `/fact-check`, and `/analyze-event`. |
| Story 8 | Application Entry Point | Configure `main.py` as the application entry point that initializes and connects all backend services. |

---

## Epic 3: Main Application Logic

**Goal:** Define the architectural principles governing how the backend services communicate and handle requests.

| Story | Task | Description |
|---|---|---|
| Story 1 | Centralized Routing Architecture | Implement a centralized routing system in FastAPI that directs all incoming requests to the appropriate service handler. |
| Story 2 | Service Layer Design Principles | Establish clear separation between API route logic and business logic, ensuring each service is modular and independently testable. |
| Story 3 | FastAPI-Specific Features Integration | Leverage FastAPI features such as automatic data validation (Pydantic models), dependency injection, and auto-generated Swagger UI documentation. |

---

## Epic 4: Frontend UI Using Streamlit

**Goal:** Design and build an interactive, user-friendly frontend that connects to the FastAPI backend.

| Story | Task | Description |
|---|---|---|
| Story 1 | Application Setup and Configuration | Set up the Streamlit app structure, page configuration, title, layout, and backend connection settings. |
| Story 2 | Input Section and Main Generation Flow | Build the input section where users enter their event description and interests, and trigger conversation starter generation. |
| Story 3 | Results Display and Feedback System | Display generated conversation starters and implement thumbs up/down feedback buttons for each result. |
| Story 4 | Fact-Checking Section | Build the fact-check input area where users can query a topic and view a summarized Wikipedia result. |
| Story 5 | Conversation History View | Build the history view that fetches and displays previously generated conversations from `history.json`. |
| Story 6 | Feedback History View | Build the feedback history view that shows which past suggestions were marked as useful by the user. |
| Story 7 | Streamlit State Management | Implement Streamlit session state to manage UI state across interactions without losing data on re-runs. |

---

## Epic 5: Testing and Local Deployment

**Goal:** Validate all components through unit testing and integration testing, then deploy the application locally.

| Story | Task | Description |
|---|---|---|
| Story 1 | Testing Philosophy & Framework Selection | Define the testing strategy using Pytest for unit tests and Httpx TestClient for API endpoint testing. |
| Story 2 | Event Analyzer Service Testing | Write and run unit tests for `event_analyzer.py` to verify correct theme extraction from sample inputs. |
| Story 3 | Topic Generator Service Testing | Write and run unit tests for `topic_generator.py` to verify GPT-2 generates valid, non-empty conversation starters. |
| Story 4 | Fact Checker Service Testing | Write and run unit tests for `fact_checker.py` to verify Wikipedia API queries return valid results. |
| Story 5 | API Routes Testing with httpx TestClient | Test all FastAPI endpoints (`/generate-conversation`, `/fact-check`, `/analyze-event`) using the httpx TestClient. |
| Story 6 | Running Tests and Interpreting Results | Execute the full test suite using `pytest`, interpret pass/fail results, and document coverage. |
| Story 7 | Local Deployment | Deploy the Streamlit frontend at `http://localhost:8501` and the FastAPI backend with Swagger UI at `http://localhost:8000/docs`. |
| Story 8 | Manual Testing and Verification | Manually test all three core scenarios: generating conversation starters, fact-checking a topic, and reviewing conversation history. |

---

## Development Flow Summary

```
1. Set up environment & select models          (Epic 1)
        ↓
2. Build all backend services & API routes     (Epic 2)
        ↓
3. Define routing & service layer principles   (Epic 3)
        ↓
4. Build the Streamlit frontend UI             (Epic 4)
        ↓
5. Test everything & deploy locally            (Epic 5)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Models | DistilBERT (theme extraction), GPT-2 Small (text generation) |
| Fact Verification | Wikipedia API (Python wrapper) |
| Testing | Pytest, Httpx |
| Data Storage | Local JSON files (`history.json`, `feedback.json`) |
| Version Control | Git & GitHub |