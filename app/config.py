"""
config.py

Centralized configuration for the Personalized Networking Assistant backend.
Keeps file paths, model names, and tunable settings in one place so other
modules never hardcode strings/paths directly.
"""

import os
from pathlib import Path


class Settings:
    # ---- Base paths ----
    BASE_DIR: Path = Path(__file__).resolve().parent.parent  # project root
    DATA_DIR: Path = BASE_DIR / "data"

    HISTORY_FILE: Path = DATA_DIR / "history.json"
    FEEDBACK_FILE: Path = DATA_DIR / "feedback.json"

    # ---- AI Models ----
    ZERO_SHOT_MODEL_NAME: str = os.getenv(
        "ZERO_SHOT_MODEL_NAME", "distilbert-base-uncased-mnli"
    )
    TEXT_GENERATION_MODEL_NAME: str = os.getenv(
        "TEXT_GENERATION_MODEL_NAME", "gpt2"
    )

    # ---- Wikipedia / Fact Checking ----
    WIKIPEDIA_LANG: str = os.getenv("WIKIPEDIA_LANG", "en")
    WIKIPEDIA_SUMMARY_SENTENCES: int = int(
        os.getenv("WIKIPEDIA_SUMMARY_SENTENCES", "3")
    )
    WIKIPEDIA_MAX_DISAMBIGUATION_ATTEMPTS: int = int(
        os.getenv("WIKIPEDIA_MAX_DISAMBIGUATION_ATTEMPTS", "3")
    )

    # ---- App-level settings ----
    APP_NAME: str = "Personalized Networking Assistant"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def ensure_data_files_exist(self) -> None:
        """
        Make sure data/history.json and data/feedback.json exist.
        Called once at app startup so logger modules can assume
        the files are always present.
        """
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

        for file_path in (self.HISTORY_FILE, self.FEEDBACK_FILE):
            if not file_path.exists():
                file_path.write_text("[]", encoding="utf-8")


# Singleton instance imported everywhere else, e.g.:
#   from app.config import settings
settings = Settings()