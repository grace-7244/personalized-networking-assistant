# 🤝 Personalized Networking Assistant

An AI-powered web application that helps users generate smart, tailored conversation starters for professional and social networking events. Built using **DistilBERT**, **GPT-2**, **FastAPI**, and **Streamlit**.

---

## 📌 Project Overview

The Personalized Networking Assistant takes an event description and user interests as input, extracts key themes using DistilBERT, and generates context-aware conversation starters using GPT-2. It also provides real-time fact-checking via the Wikipedia API and allows users to log conversation history and provide feedback on suggestions.

### Core Features

- 🧠 **AI Conversation Starter Generation** — DistilBERT extracts event themes; GPT-2 generates starters
- ✅ **Fact Checking** — Wikipedia API provides reliable, summarized references
- 📜 **Conversation History** — Past sessions saved locally and reviewable anytime
- 👍 **Feedback System** — Thumbs up/down on suggestions for continuous improvement
- 📄 **Auto API Docs** — Swagger UI generated automatically via FastAPI

---

## 🧑‍💻 Team

| Name | Role |
|---|---|
| Sowmya | Team Leader — Architecture, Documentation, Backend Logic |
| Varshitha | AI Models, Core Services, Testing |
| Kyathi | Data Services, API Routes, Frontend Config |
| Jessica | Streamlit UI, Deployment, Integration Testing |

---

## 🏗️ Project Architecture

```
personalized-networking-assistant/
│
├── app/
│   ├── models/
│   │   └── schemas.py          # Pydantic request/response models
│   ├── routers/
│   │   └── conversation.py     # FastAPI route definitions
│   ├── services/
│   │   ├── event_analyzer.py   # DistilBERT theme extraction
│   │   ├── topic_generator.py  # GPT-2 conversation generation
│   │   ├── fact_checker.py     # Wikipedia API fact checking
│   │   ├── history_logger.py   # Conversation history persistence
│   │   └── feedback_logger.py  # User feedback persistence
│   ├── config.py               # App configuration
│   └── main.py                 # Application entry point
│
├── tests/
│   ├── conftest.py             # Shared pytest fixtures
│   ├── test_event_analyzer.py  # Event analyzer unit tests
│   ├── test_topic_generator.py # Topic generator unit tests
│   ├── test_fact_checker.py    # Fact checker unit tests
│   └── test_routes.py          # API route integration tests
│
├── frontend/
│   └── streamlit_app.py        # Streamlit UI
│
├── data/
│   ├── history.json            # Saved conversation history
│   └── feedback.json           # Saved user feedback
│
├── docs/                       # Project documentation
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Theme Extraction | DistilBERT (Hugging Face Transformers) |
| Text Generation | GPT-2 Small (Hugging Face Transformers) |
| Fact Verification | Wikipedia API (Python wrapper) |
| Data Persistence | Local JSON files |
| Testing | Pytest + Httpx |
| Version Control | Git & GitHub |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/personalized-networking-assistant.git
cd personalized-networking-assistant
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend will be running at:
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

### 5. Run the Streamlit Frontend

Open a **new terminal** (keep the backend running) and run:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will be running at: `http://localhost:8501`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check — confirms API is running |
| `POST` | `/analyze-event` | Extract themes from an event description |
| `POST` | `/generate-conversation` | Generate AI conversation starters |
| `POST` | `/fact-check` | Fact-check a topic via Wikipedia |

### Example Request — Generate Conversation

```bash
POST http://localhost:8000/generate-conversation
Content-Type: application/json

{
    "description": "AI for Sustainable Cities",
    "interests": ["climate change", "urban planning"]
}
```

### Example Response

```json
{
    "topics": ["artificial intelligence", "sustainability", "urban development"],
    "suggestions": [
        "How do you see AI transforming urban infrastructure in the next decade?",
        "What role do you think machine learning plays in reducing city carbon footprints?",
        "Have you worked on any projects connecting smart city tech with climate goals?"
    ]
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with detailed output
pytest -v

# Run a specific test file
pytest tests/test_event_analyzer.py -v
```

---

## 📖 User Scenarios

### Scenario 1 — Generating Smart Starters
A user enters an event description such as *"AI for Sustainable Cities"* and interests like *"climate change"* and *"urban planning"*. The assistant extracts themes and generates 2–3 tailored conversation starters.

### Scenario 2 — Quick Fact Verification
A user preparing for a conference searches for a quick fact check on *"blockchain in healthcare"*. The app returns a summarized, reliable reference from Wikipedia.

### Scenario 3 — Reviewing Past Strategies
A user accesses the History section to review previously generated conversations and which ones were marked useful — encouraging continuous improvement in networking skills.

---

## 📂 Documentation

All project documentation is available in the `docs/` folder:

| File | Description |
|---|---|
| `er_diagram.md` | Entity-Relationship diagram description |
| `project_workflow.md` | Full Epic and Story breakdown |
| `application_architecture.md` | Three-tier architecture and directory design |
| `data_schema.md` | Pydantic schema definitions and usage |
| `application_entry_point.md` | main.py structure and design decisions |
| `centralized_routing.md` | Hub-and-spoke routing architecture |
| `service_layer_design.md` | Service layer design principles |
| `fastapi_features.md` | FastAPI-specific features leveraged |
| `conclusion.md` | Project summary, outcomes, and future scope |

---

## 🔮 Future Scope

- User authentication and per-user history
- Database integration (SQLite or PostgreSQL)
- Upgraded language models (GPT-Neo, LLaMA)
- Feedback-driven personalization
- Cloud deployment (Render + Streamlit Cloud)
- Multi-language support

---
