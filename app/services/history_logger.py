"""
history_logger.py

Handles reading and writing conversation session history to
data/history.json. Each entry represents one generated conversation
session (description, interests, resulting topics/suggestions, timestamp).
"""

import json
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.config import settings

logger = logging.getLogger(__name__)

# Simple in-process lock to avoid concurrent read/modify/write races
# on the JSON file when FastAPI handles requests concurrently.
_lock = threading.Lock()


def _read_all() -> List[Dict[str, Any]]:
    """Read the full history list from disk. Returns [] on any problem."""
    try:
        with open(settings.HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            logger.warning("history.json did not contain a list; resetting.")
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        logger.warning("history.json was corrupted/unreadable; resetting.")
        return []


def _write_all(entries: List[Dict[str, Any]]) -> None:
    """Write the full history list to disk, pretty-printed."""
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(settings.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def save_history_entry(
    description: str,
    interests: List[str],
    topics: List[str],
    suggestions: List[str],
) -> Dict[str, Any]:
    """
    Append a new conversation session to history.json.

    Returns the entry that was saved (including its generated id/timestamp),
    which callers can use directly in a response if needed.
    """
    entry = {
        "id": _next_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": description,
        "interests": interests,
        "topics": topics,
        "suggestions": suggestions,
    }

    with _lock:
        entries = _read_all()
        entries.append(entry)
        _write_all(entries)

    return entry


def load_history(limit: int = None) -> List[Dict[str, Any]]:
    """
    Load conversation history, most recent last (insertion order).

    Args:
        limit: if provided, only return the most recent `limit` entries.
    """
    with _lock:
        entries = _read_all()

    if limit is not None:
        return entries[-limit:]
    return entries


def clear_history() -> None:
    """Wipe all history (useful for tests / admin reset)."""
    with _lock:
        _write_all([])


def _next_id() -> int:
    """Generate the next sequential integer id based on current entries."""
    entries = _read_all()
    if not entries:
        return 1
    existing_ids = [e.get("id", 0) for e in entries if isinstance(e.get("id"), int)]
    return (max(existing_ids) + 1) if existing_ids else len(entries) + 1