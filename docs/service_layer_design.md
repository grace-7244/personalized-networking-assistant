# Service Layer Design Principles — Personalized Networking Assistant

## Overview

The service layer is the core of the application's business logic. It sits between the API routes and the AI models, keeping route handlers thin and ensuring all logic is modular, testable, and easy to maintain.

The service layer is designed around three key software engineering principles:

---

## Principle 1: Single Responsibility Principle

Each service file has **exactly one job**:

| Service File | Single Responsibility |
|---|---|
| `event_analyzer.py` | Theme extraction from event descriptions only |
| `topic_generator.py` | Conversation starter text generation only |
| `fact_checker.py` | Wikipedia API querying and summarization only |
| `history_logger.py` | Reading and writing conversation history only |
| `feedback_logger.py` | Reading and writing user feedback only |

### Why This Matters

If the fact-checking mechanism needs to change — for example, switching from Wikipedia to a different API — **only `fact_checker.py` needs to be modified**. All other service files, routes, and tests remain completely untouched.

```
Change needed: Switch fact-check source from Wikipedia → DuckDuckGo API

Files that change:  fact_checker.py  ✏️  (1 file only)
Files untouched:    event_analyzer.py  ✅
                    topic_generator.py ✅
                    history_logger.py  ✅
                    feedback_logger.py ✅
                    conversation.py    ✅
                    main.py            ✅
```

---

## Principle 2: Dependency Injection via Imports

Services are imported at the **top of `conversation.py`**, making all dependencies explicit and easy to identify at a glance:

```python
# app/routers/conversation.py

from app.services.event_analyzer import analyze_event
from app.services.topic_generator import generate_conversation
from app.services.fact_checker import fact_check
```

### Why This Matters

- Dependencies are visible immediately — no hidden wiring or global state
- In testing scenarios, these imports can be **mocked** to test route logic in complete isolation from the actual AI models
- This is critical because loading DistilBERT and GPT-2 in every test run would make tests **prohibitively slow**

```python
# Example: Mocking the AI service in a test
from unittest.mock import patch

def test_generate_conversation_route():
    with patch("app.routers.conversation.generate_conversation") as mock_gen:
        mock_gen.return_value = ["Great opener!", "Tell me about your work"]
        # Test the route logic without ever loading GPT-2
```

---

## Principle 3: Stateless Service Functions

All service functions are **stateless** — they take input parameters and return output without modifying any shared state:

```
Input → [ Service Function ] → Output
         (no side effects)
```

### Stateless Services (AI Services)

| Function | Input | Output | State Modified? |
|---|---|---|---|
| `analyze_event(description)` | Event text string | List of theme strings | ❌ None |
| `generate_conversation(description, interests)` | Text + interests list | List of starter strings | ❌ None |
| `fact_check(query)` | Query string | Summary string | ❌ None |

### Stateful Services (Logger Services — intentional exception)

| Function | Input | Output | State Modified? |
|---|---|---|---|
| `save_to_history(entry)` | Conversation entry | Confirmation | ✅ `history.json` |
| `save_feedback(entry)` | Feedback entry | Confirmation | ✅ `feedback.json` |

The logger functions **intentionally maintain state** in JSON files — that is their entire purpose. This is a deliberate design choice, not a violation of the principle.

### Why Statelessness Matters for Testing

Stateless functions are **trivially testable**:

```python
# Stateless function — easy to test
def test_fact_check():
    result = fact_check("blockchain in healthcare")
    assert isinstance(result, str)
    assert len(result) > 0
    # Same input always produces a valid output — no setup or teardown needed
```

- Given the same inputs, stateless functions always produce **deterministic outputs** (loggers) or **model-dependent outputs** (AI services)
- No database to reset, no shared memory to clear, no global variables to worry about
- Tests can run in any order without interfering with each other

---

## Service Layer Structure

```
app/
└── services/
    ├── event_analyzer.py     # Stateless — DistilBERT theme extraction
    ├── topic_generator.py    # Stateless — GPT-2 text generation
    ├── fact_checker.py       # Stateless — Wikipedia API queries
    ├── history_logger.py     # Stateful  — reads/writes history.json
    └── feedback_logger.py    # Stateful  — reads/writes feedback.json
```

---

## Summary

| Principle | Applied As | Benefit |
|---|---|---|
| Single Responsibility | One job per service file | Changes are isolated — modify one file, nothing else breaks |
| Dependency Injection | Explicit imports at top of router | Dependencies are visible; easy to mock in tests |
| Stateless Functions | No shared state in AI services | Functions are predictable, isolated, and fast to test |