# Application Entry Point — Personalized Networking Assistant

## Overview

The `app/main.py` file is the entry point of the entire FastAPI backend application. It is **intentionally minimal**, following the principle of *doing one thing well* — its only responsibilities are to create the app instance, register routers, and expose a health-check endpoint.

All business logic lives in the service layer. All route logic lives in the routers. `main.py` simply connects them together.

---

## File Location

```
app/
└── main.py   ← application entry point
```

---

## Full Code

```python
# app/main.py

from fastapi import FastAPI
from app.routers import conversation

app = FastAPI(title="Personalized Networking Assistant")
app.include_router(conversation.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Networking Assistant API!"}
```

---

## Line-by-Line Breakdown

### Imports
```python
from fastapi import FastAPI
from app.routers import conversation
```
- Imports the `FastAPI` class to create the application instance
- Imports the `conversation` router module which contains all three API endpoint definitions

---

### App Initialization
```python
app = FastAPI(title="Personalized Networking Assistant")
```
- Creates the FastAPI application instance
- The `title` parameter appears in the **auto-generated Swagger UI** at `http://localhost:8000/docs`, making the API self-documenting out of the box

---

### Router Registration
```python
app.include_router(conversation.router)
```
- Registers the conversation router with the main app
- This single line brings in **all three API endpoints** defined in `app/routers/conversation.py`:
  - `POST /generate-conversation`
  - `POST /fact-check`
  - `POST /analyze-event`

---

### Health-Check Endpoint
```python
@app.get("/")
def root():
    return {"message": "Welcome to the Networking Assistant API!"}
```
- Defines a simple `GET /` root endpoint
- This is a **production best practice** — it allows developers, load balancers, and monitoring systems to quickly verify the API is running and reachable before making any business-logic calls
- Returns a plain JSON message confirming the server is online

---

## How to Run

Start the FastAPI backend server with:

```bash
uvicorn app.main:app --reload
```

| URL | Purpose |
|---|---|
| `http://localhost:8000/` | Health-check — confirms server is running |
| `http://localhost:8000/docs` | Swagger UI — interactive API documentation |
| `http://localhost:8000/redoc` | ReDoc — alternative API documentation view |

---

## Design Decision — Why Keep main.py Minimal?

| Concern | How It Is Handled |
|---|---|
| Business logic | Lives in `app/services/` |
| Route definitions | Live in `app/routers/conversation.py` |
| Configuration | Lives in `app/config.py` |
| Data models | Live in `app/models/schemas.py` |
| App wiring | `main.py` — imports and registers only |

Keeping `main.py` minimal means the entry point never needs to change when new features are added — only a new `include_router()` call is needed to plug in additional functionality.