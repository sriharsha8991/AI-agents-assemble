from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.services.gemini_client import GeminiClient
from src.storage.resume_store import save_parsed_resume


app = FastAPI(title="Resume Structuring Service")


@app.post("/resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload one or more resume files and store structured JSON outputs.

    Accepts PDF, DOCX, and TXT files. Each file is sent to Gemini API for
    structured extraction and the resulting JSON is stored on disk.

    Returns a list of results with per-file status and ID.
    """

    allowed_content_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }

    try:
        client = GeminiClient()
    except RuntimeError as exc:  # missing API key
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    results = []

    for file in files:
        if file.content_type not in allowed_content_types:
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "detail": "Unsupported file type. Please upload pdf, docx, or txt.",
                }
            )
            continue

        try:
            file_bytes = await file.read()
            
            # Determine file extension from original filename
            suffix = Path(file.filename).suffix or ".tmp"
            
            # Write to a temporary file with the correct extension so Gemini can infer MIME type
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            
            try:
                resume = client.extract_resume(tmp_path)
                resume_id = save_parsed_resume(resume)
                results.append(
                    {
                        "filename": file.filename,
                        "id": resume_id,
                        "status": "success",
                    }
                )
            finally:
                # Clean up temporary file
                Path(tmp_path).unlink(missing_ok=True)
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "detail": f"Failed to process resume: {exc}",
                }
            )

    return JSONResponse(results)
