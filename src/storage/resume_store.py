from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict

from src.models.resume import Resume


BASE_DIR = Path(__file__).resolve().parents[2]
PARSED_DIR = BASE_DIR / "data" / "resumes" / "parsed"


def ensure_storage_dirs() -> None:
    PARSED_DIR.mkdir(parents=True, exist_ok=True)


def save_parsed_resume(resume: Resume) -> str:
    """Persist the structured resume JSON and return its generated ID."""
    ensure_storage_dirs()
    resume_id = str(uuid.uuid4())
    output_path = PARSED_DIR / f"{resume_id}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(resume.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

    return resume_id


def load_parsed_resume(resume_id: str) -> Dict[str, Any]:
    """Load previously stored structured resume JSON by ID."""
    path = PARSED_DIR / f"{resume_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No stored resume with id {resume_id}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
