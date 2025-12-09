from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Union

from google import genai
from pydantic import BaseModel


# Path to prompts configuration
PROMPTS_PATH = Path(__file__).resolve().parents[1] / "config" / "prompts.json"


def load_prompts() -> Dict[str, Any]:
    """Load prompts configuration from JSON file."""
    with PROMPTS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


class GeminiClient:
    """Wrapper around google-genai client for various LLM services."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash") -> None:
        # Prefer explicit api_key but allow environment variable fallback.
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

        # Configure client
        os.environ["GOOGLE_API_KEY"] = self._api_key
        self._client = genai.Client()
        self._model = model
        self._prompts = load_prompts()

    def extract_resume(self, file_path: Union[str, Path], schema: type[BaseModel]) -> BaseModel:
        """Upload a resume file to Gemini and return a structured Resume.

        Parameters
        ----------
        file_path: str | Path
            Path to the resume file. The file extension is used by Gemini to infer MIME type.
        schema: type[BaseModel]
            Pydantic model class defining the expected output schema.

        Returns
        -------
        BaseModel
            Parsed response matching the provided schema.
        """
        prompts = self._prompts.get("resume_extraction", {})
        system_instruction = prompts.get("system_instruction", "")
        user_prompt = prompts.get("user_prompt", "")

        # Upload file using Files API
        uploaded_file = self._client.files.upload(file=str(file_path))

        response = self._client.models.generate_content(
            model=self._model,
            contents=[user_prompt, uploaded_file],
            config={
                "response_mime_type": "application/json",
                "response_json_schema": schema.model_json_schema(),
                "system_instruction": system_instruction,
            },
        )

        return schema.model_validate_json(response.text)

    def score_resume_ats(
        self,
        resume_data: Dict[str, Any],
        job_description: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        """Score a resume against a job description using ATS criteria.

        Parameters
        ----------
        resume_data: Dict[str, Any]
            Structured resume JSON data (from parsed resume).
        job_description: str
            Job description text to compare against.
        schema: type[BaseModel]
            Pydantic model class defining the expected ATS score output schema.

        Returns
        -------
        BaseModel
            Parsed ATS score response matching the provided schema.
        """
        prompts = self._prompts.get("ats_scoring", {})
        system_instruction = prompts.get("system_instruction", "")
        user_prompt_template = prompts.get("user_prompt", "")

        # Format the prompt with resume and job description
        resume_json_str = json.dumps(resume_data, indent=2, ensure_ascii=False)
        user_prompt = user_prompt_template.format(
            resume_json=resume_json_str,
            job_description=job_description,
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=[user_prompt],
            config={
                "response_mime_type": "application/json",
                "response_json_schema": schema.model_json_schema(),
                "system_instruction": system_instruction,
            },
        )

        return schema.model_validate_json(response.text)
