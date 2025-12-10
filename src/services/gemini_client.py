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
    try:
        with PROMPTS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(
            f"Prompts configuration file not found at {PROMPTS_PATH}. "
            "Ensure config/prompts.json exists in the project root."
        )
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Invalid JSON in prompts configuration file {PROMPTS_PATH}: {e}"
        )

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
        prompts = self._prompts.get("resume_extraction")
        if not prompts:
            raise ValueError(
                "Missing 'resume_extraction' configuration in prompts file"
            )
        
        system_instruction = prompts.get("system_instruction")
        user_prompt = prompts.get("user_prompt")
        
        if not system_instruction or not user_prompt:
            raise ValueError(
                "Missing required prompts: both 'system_instruction' and 'user_prompt' "
                "must be present in resume_extraction configuration"
            )
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
        
        Raises
        ------
        ValueError
            If required prompts are missing or invalid, or if prompt formatting fails.
        """
        # Validate that ats_scoring prompts exist
        prompts = self._prompts.get("ats_scoring")
        if not prompts:
            raise ValueError(
                "Missing 'ats_scoring' configuration in prompts.json. "
                "Please ensure the prompts configuration file contains an 'ats_scoring' section."
            )
        
        # Validate required prompt fields are present and non-empty
        system_instruction = prompts.get("system_instruction", "").strip()
        user_prompt_template = prompts.get("user_prompt", "").strip()
        
        if not system_instruction:
            raise ValueError(
                "Missing or empty 'system_instruction' in ats_scoring prompts. "
                "Please provide a valid system instruction in prompts.json."
            )
        
        if not user_prompt_template:
            raise ValueError(
                "Missing or empty 'user_prompt' in ats_scoring prompts. "
                "Please provide a valid user prompt template in prompts.json."
            )

        # Format the prompt with resume and job description
        resume_json_str = json.dumps(resume_data, indent=2, ensure_ascii=False)
        
        try:
            user_prompt = user_prompt_template.format(
                resume_json=resume_json_str,
                job_description=job_description,
            )
        except KeyError as e:
            missing_placeholder = str(e).strip("'")
            raise ValueError(
                f"Missing required placeholder '{missing_placeholder}' in user_prompt template. "
                f"Expected placeholders: 'resume_json', 'job_description'. "
                f"Template content: {user_prompt_template[:200]}..."
            ) from e

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
