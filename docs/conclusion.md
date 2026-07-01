# Conclusion — Personalized Networking Assistant

## Project Summary

The Personalized Networking Assistant is an AI-powered web application designed to help users generate smart, context-aware conversation starters for professional and social networking events. Built collaboratively by a four-member team over the course of the project, the application successfully integrates modern NLP models, a modular REST API backend, an interactive frontend, and a robust testing suite — all running locally without the need for any external database or paid cloud service.

This document summarizes the key work completed across all five epics, reflects on the outcomes achieved, and outlines the scope for future development.

---

## Work Completed

### Epic 1: Model Selection and Architecture
The project began with thorough research into available NLP models on the Hugging Face ecosystem. **DistilBERT** was selected for zero-shot event theme classification due to its speed and efficiency, while **GPT-2 Small** was chosen for human-like conversation starter generation. A clean three-tier architecture was defined — separating the Streamlit frontend, FastAPI backend, and AI service layer — along with a modular directory structure that allowed all four team members to work independently without conflicts.

### Epic 2: Core Functionalities Development
The backbone of the application was built in this phase. Six Pydantic schemas were defined to govern all data exchange between the frontend and backend. Five independent service modules were implemented:

- `event_analyzer.py` — extracts themes from event descriptions using DistilBERT
- `topic_generator.py` — generates conversation starters using GPT-2
- `fact_checker.py` — retrieves and summarizes factual references via the Wikipedia API
- `history_logger.py` — persists all generated conversations to `history.json`
- `feedback_logger.py` — records user thumbs up/down feedback to `feedback.json`

Three FastAPI routes (`/generate-conversation`, `/fact-check`, `/analyze-event`) were implemented and connected through a centralized routing architecture, with `main.py` serving as the clean application entry point.

### Epic 3: Main Application Logic
The backend's architectural principles were defined and implemented. A hub-and-spoke routing model was adopted, with `main.py` as the central hub and `conversation.py` as the route spoke. The Single Responsibility Principle, Dependency Injection via imports, and Stateless Service Functions were applied throughout the service layer — ensuring the codebase is maintainable, modular, and easy to extend. FastAPI-specific features including automatic OpenAPI documentation, type-safe request validation, and response model enforcement were fully leveraged.

### Epic 4: Frontend UI Using Streamlit
A complete, interactive Streamlit frontend was built with the following sections:

- **Input section** — event description and user interests entry
- **Generation flow** — triggers `/generate-conversation` and displays results
- **Feedback system** — thumbs up/down buttons on each generated starter
- **Fact-checking section** — dedicated input to query the `/fact-check` endpoint
- **Conversation history view** — displays all past sessions from `history.json`
- **Feedback history view** — shows which suggestions were marked useful

Streamlit session state was implemented throughout to preserve UI state across interactions without data loss on re-runs.

### Epic 5: Testing and Local Deployment
A comprehensive testing suite was developed using **Pytest** for unit testing and **Httpx TestClient** for API endpoint testing. Individual unit tests were written for the event analyzer, topic generator, and fact checker services. All three FastAPI routes were tested for correct request handling, response structure, and error cases. The full test suite was executed and results documented. The application was successfully deployed locally with the Streamlit frontend running at `http://localhost:8501` and the FastAPI backend with Swagger UI at `http://localhost:8000/docs`. All three core user scenarios — generating starters, fact-checking, and reviewing history — were manually verified end to end.

---

## Key Outcomes

| Outcome | Detail |
|---|---|
| Working AI-powered application | End-to-end app generating real conversation starters using DistilBERT + GPT-2 |
| Modular backend | Five independent, testable service modules with zero tight coupling |
| Self-documenting API | Swagger UI auto-generated from Pydantic models with no extra configuration |
| Interactive frontend | Full Streamlit UI covering all three core user scenarios |
| Local data persistence | Conversation history and feedback stored in JSON without any database |
| Test coverage | Unit tests for all core services and integration tests for all API routes |
| Successful local deployment | Both frontend and backend running and verified locally |

---

## Team Contributions

| Member | Role | Primary Responsibilities |
|---|---|---|
| **Sowmya** | Team Leader | Project architecture, ER diagram, workflow, data schema, application entry point, backend logic documentation, conclusion |
| **Varshitha** | Member 1 | Model research and selection, environment setup, event analyzer service, topic generator service, testing philosophy, event analyzer and topic generator tests |
| **Kyathi** | Member 2 | Fact checker service, history logger, feedback logger, API routes, Streamlit app setup, state management, fact checker tests, test results documentation |
| **Jessica** | Member 3 | Full Streamlit frontend UI (all five sections), API route testing with httpx, local deployment, manual testing and verification |

---

## Challenges and Learning Outcomes

Through the development of this project, the team gained hands-on experience with:

- **Transformer-based NLP models** — loading, running, and integrating DistilBERT and GPT-2 using the Hugging Face Transformers library
- **FastAPI development** — building production-style REST APIs with automatic validation, serialization, and documentation
- **Streamlit frontend development** — building reactive, stateful web UIs entirely in Python
- **Software engineering principles** — applying Single Responsibility, Dependency Injection, and Stateless Design in a real project
- **Collaborative development** — working across a modular codebase with clearly defined ownership boundaries for each team member
- **Testing practices** — writing meaningful unit tests and using mock objects to isolate AI-heavy services during testing

---

## Future Scope

While the current implementation fulfills all project requirements, several enhancements could extend the application further:

| Enhancement | Description |
|---|---|
| User authentication | Add login/signup so each user's history and feedback are stored separately |
| Database integration | Replace JSON files with SQLite or PostgreSQL for scalable data persistence |
| Improved AI models | Upgrade from GPT-2 to a larger model (e.g., GPT-Neo or a fine-tuned LLaMA variant) for higher quality conversation starters |
| Feedback-driven personalization | Use accumulated feedback data to fine-tune suggestions for individual users over time |
| Cloud deployment | Deploy the FastAPI backend on Render or Railway and the Streamlit app on Streamlit Cloud for public access |
| Multi-language support | Extend the application to generate conversation starters in languages other than English |

---

## Final Reflection

The Personalized Networking Assistant successfully demonstrates how modern NLP models can be integrated into a practical, user-facing application using a clean and maintainable software architecture. The project achieves its core goal — helping users walk into any networking event with well-prepared, intelligent conversation starters tailored to the event's themes and their own interests.

The modular design adopted throughout the project ensures the application is not just a one-time deliverable but a solid foundation that can be extended with new features, better models, and production-grade infrastructure as requirements evolve.

> *Built with FastAPI, Streamlit, DistilBERT, GPT-2, and Wikipedia API.*
> *Developed by Sowmya, Varshitha, Kyathi, and Jessica.*