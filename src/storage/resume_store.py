from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

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


def _hash_job_description(job_description: str) -> str:
    """Generate a stable hash for job description to use as cache key."""
    return hashlib.sha256(job_description.strip().encode("utf-8")).hexdigest()[:32]

def get_cached_ats_score(resume_id: str, job_description: str) -> Optional[Dict[str, Any]]:
    """Retrieve cached ATS score for a resume-job combination.
    
    Parameters
    ----------
    resume_id: str
        UUID of the stored resume.
    job_description: str
        Job description text.
    
    Returns
    -------
    Optional[Dict[str, Any]]
        Cached ATS score if found, None otherwise.
    """
    path = PARSED_DIR / f"{resume_id}.json"
    if not path.exists():
        return None
    
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Check if ats_scores field exists
    ats_scores = data.get("ats_scores", {})
    job_hash = _hash_job_description(job_description)
    
    return ats_scores.get(job_hash)


import tempfile

def save_ats_score(
    resume_id: str,
    job_description: str,
    ats_score: Dict[str, Any],
) -> None:
    """Save ATS score to resume JSON file for caching.
    
    Parameters
    ----------
    resume_id: str
        UUID of the stored resume.
    job_description: str
        Job description text used for scoring.
    ats_score: Dict[str, Any]
        ATS score data to cache.
    """
    path = PARSED_DIR / f"{resume_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No stored resume with id {resume_id}")
    
    # Load existing data
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Initialize ats_scores if not present
    if "ats_scores" not in data:
        data["ats_scores"] = {}
    
    # Add new score with job description hash as key
    job_hash = _hash_job_description(job_description)
    data["ats_scores"][job_hash] = {
        "job_description_hash": job_hash,
        "job_description_preview": job_description[:200] + "..." if len(job_description) > 200 else job_description,
        "score": ats_score,
    }
    
    # Atomic write: write to temp file, then rename
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except:
        os.unlink(tmp_path)
        raise