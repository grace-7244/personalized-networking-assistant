# app/services/feedback_logger.py

"""
feedback_logger.py
Handles reading and writing user feedback (thumbs up / thumbs down on
generated conversation suggestions) to data/feedback.json.
"""

import json
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.config import settings

logger = logging.getLogger(__name__)
_lock = threading.Lock()


def _read_all() -> List[Dict[str, Any]]:
    """Read the full feedback list from disk. Returns [] on any problem."""
    try:
        with open(settings.FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            logger.warning("feedback.json did not contain a list; resetting.")
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        logger.warning("feedback.json was corrupted/unreadable; resetting.")
        return []


def _write_all(entries: List[Dict[str, Any]]) -> None:
    """Write the full feedback list to disk, pretty-printed."""
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(settings.FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _next_id() -> int:
    """Generate the next sequential integer id based on current entries."""
    entries = _read_all()
    if not entries:
        return 1
    existing_ids = [e.get("id", 0) for e in entries if isinstance(e.get("id"), int)]
    return (max(existing_ids) + 1) if existing_ids else len(entries) + 1


def save_feedback(
    suggestion: str,
    rating: str,                      # "positive" or "negative" — matches streamlit_app.py
    history_id: Optional[int] = None,
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Save a single piece of user feedback.

    Args:
        suggestion: the conversation-starter text being rated.
        rating: "positive" for thumbs up, "negative" for thumbs down.
                Matches the value sent by streamlit_app.py.
        history_id: optional link back to a history.json entry id.
        comment: optional free-text comment from the user.

    Returns:
        The saved entry dict including id and timestamp.
    """
    entry = {
        "id": _next_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "history_id": history_id,
        "suggestion": suggestion,
        "rating": rating,                          # "positive" | "negative"
        "is_positive": rating == "positive",       # boolean convenience field
        "comment": comment,
    }
    with _lock:
        entries = _read_all()
        entries.append(entry)
        _write_all(entries)
    return entry


def load_feedback(limit: int = None) -> List[Dict[str, Any]]:
    """Load all feedback entries, optionally limited to the most recent N."""
    with _lock:
        entries = _read_all()
    if limit is not None:
        return entries[-limit:]
    return entries


def get_feedback_summary() -> Dict[str, int]:
    """Quick aggregate: counts of positive vs negative feedback."""
    entries = load_feedback()
    positive = sum(1 for e in entries if e.get("rating") == "positive")
    negative = sum(1 for e in entries if e.get("rating") == "negative")
    return {"positive": positive, "negative": negative, "total": len(entries)}


def clear_feedback() -> None:
    """Wipe all feedback (useful for tests / admin reset)."""
    with _lock:
        _write_all([])