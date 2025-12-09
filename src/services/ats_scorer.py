from __future__ import annotations

from typing import Dict, Any

from src.models.ats_score import ATSScore
from src.services.gemini_client import GeminiClient
from src.storage.resume_store import (
    load_parsed_resume,
    get_cached_ats_score,
    save_ats_score,
)


class ATSScorer:
    """Service for scoring resumes against job descriptions using ATS criteria."""

    def __init__(self, gemini_client: GeminiClient | None = None) -> None:
        """Initialize ATS scorer with a Gemini client.

        Parameters
        ----------
        gemini_client: GeminiClient | None
            Optional pre-configured Gemini client. If None, a new one is created.
        """
        self.client = gemini_client or GeminiClient()

    def score(self, resume_id: str, job_description: str, use_cache: bool = True) -> ATSScore:
        """Score a resume against a job description.

        Parameters
        ----------
        resume_id: str
            UUID of the stored resume JSON.
        job_description: str
            Job description text to evaluate the resume against.
        use_cache: bool
            If True, check for cached score before calling Gemini API.

        Returns
        -------
        ATSScore
            Structured ATS scoring result with overall score, section scores,
            strengths, gaps, recommendations, and keyword analysis.

        Raises
        ------
        FileNotFoundError
            If no resume with the given ID exists.
        """
        # Check cache first if enabled
        if use_cache:
            cached_score = get_cached_ats_score(resume_id, job_description)
            if cached_score:
                # Return cached score, extracting the actual score data
                score_data = cached_score.get("score", cached_score)
                return ATSScore.model_validate(score_data)

        # Load the parsed resume data
        resume_data: Dict[str, Any] = load_parsed_resume(resume_id)
        
        # Remove ats_scores from resume_data before sending to Gemini
        # to avoid sending cached scores in the prompt
        resume_data_clean = {k: v for k, v in resume_data.items() if k != "ats_scores"}

        # Use Gemini to score the resume
        ats_score: ATSScore = self.client.score_resume_ats(
            resume_data=resume_data_clean,
            job_description=job_description,
            schema=ATSScore,
        )

        # Cache the result
        save_ats_score(
            resume_id=resume_id,
            job_description=job_description,
            ats_score=ats_score.model_dump(mode="json"),
        )

        return ats_score
