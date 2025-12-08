from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from google import genai

from src.models.resume import Resume


class GeminiClient:
    """Wrapper around google-genai client for resume extraction."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash") -> None:
        # Prefer explicit api_key but allow environment variable fallback.
        # According to Gemini docs, the client reads configuration from env,
        # but we also support passing it directly for clarity.
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

        # Configure client; google-genai uses environment variable under the hood,
        # so we set it explicitly here.
        os.environ["GOOGLE_API_KEY"] = self._api_key
        self._client = genai.Client()
        self._model = model

    def extract_resume(self, file_path: Union[str, Path]) -> Resume:
        """Upload a resume file to Gemini and return a structured Resume.

        Parameters
        ----------
        file_path: str | Path
            Path to the resume file. The file extension is used by Gemini to infer MIME type.
        """

        # Upload file using Files API. Pass the file path so Gemini can infer
        # the MIME type from the file extension.
        uploaded_file = self._client.files.upload(file=str(file_path))

        prompt = (
            "You are an assistant that extracts structured resume information. "
            "Analyze the provided resume file and return a JSON object that strictly "
            "conforms to the given schema. Fill in as many fields as you can "
            "based only on the resume content. Do not invent facts."
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=[prompt, uploaded_file],
            config={
                "response_mime_type": "application/json",
                "response_json_schema": Resume.model_json_schema(),
            },
        )

        # response.text should contain JSON matching the Resume schema
        return Resume.model_validate_json(response.text)
