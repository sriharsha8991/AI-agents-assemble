from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.models.resume import Resume
from src.models.ats_score import ATSScore
from src.models.insights import SalaryRecommendation, UpskillingReport
from src.services.gemini_client import GeminiClient
from src.services.ats_scorer import ATSScorer
from src.services.insights_service import InsightsService
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
                resume = client.extract_resume(tmp_path, schema=Resume)
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


class ATSScoreRequest(BaseModel):
    resume_id: str = Field(..., description="UUID of the stored resume to evaluate.")
    job_description: str = Field(..., description="Full job description text to compare against.")
    use_cache: bool = Field(
        default=True,
        description="If True, return cached score if available. Set to False to force re-evaluation.",
    )


class SalaryRecommendationRequest(BaseModel):
    """Request for salary recommendation analysis."""
    resume_id: str = Field(..., description="UUID of the resume to analyze")
    job_title: str | None = Field(
        default=None,
        description="Target job title (optional, uses resume's current role if not provided)"
    )
    location: str | None = Field(
        default=None,
        description="Target location (optional, uses resume's location if not provided)"
    )
    experience_years: int | None = Field(
        default=None,
        description="Years of experience (optional, calculated from resume if not provided)"
    )


class UpskillingRequest(BaseModel):
    """Request for upskilling recommendations."""
    resume_id: str = Field(..., description="UUID of the resume to analyze")
    job_description_hash: str | None = Field(
        default=None,
        description="Hash of job description for ATS score lookup (optional)"
    )
    target_role: str | None = Field(
        default=None,
        description="Target role for upskilling (optional, uses current role if not provided)"
    )



@app.post("/ats-score", response_model=ATSScore)
async def score_resume_ats(request: ATSScoreRequest = Body(...)):
    """Score a resume against a job description using ATS criteria.

    Accepts a resume ID (from previously uploaded resume) and a job description.
    Returns a comprehensive ATS compatibility score with detailed feedback.
    
    Results are cached in the resume JSON file. Subsequent requests with the same
    resume_id and job_description will return the cached score unless use_cache=False.

    Parameters
    ----------
    request: ATSScoreRequest
        Body containing resume_id, job_description, and optional use_cache flag.

    Returns
    -------
    ATSScore
        Detailed ATS scoring result including overall score, section scores,
        strengths, gaps, recommendations, and keyword analysis.
    """
    try:
        scorer = ATSScorer()
        ats_result = scorer.score(
            resume_id=request.resume_id,
            job_description=request.job_description,
            use_cache=request.use_cache,
        )
        return ats_result
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Resume not found: {exc}",
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail=f"Failed to score resume: {exc}",
        ) from exc


@app.post("/insights/salary-recommendation", response_model=SalaryRecommendation)
async def get_salary_recommendation(request: SalaryRecommendationRequest = Body(...)):
    """Generate salary recommendation based on market research.
    
    Uses Gemini AI to analyze market compensation data and provide
    personalized salary recommendations based on candidate profile.
    
    Parameters
    ----------
    request: SalaryRecommendationRequest
        Resume ID, optional job title, location, and experience years.
    
    Returns
    -------
    SalaryRecommendation
        Comprehensive salary analysis with market data and trends.
    """
    try:
        insights = InsightsService()
        result = insights.get_salary_recommendation(
            resume_id=request.resume_id,
            job_title=request.job_title,
            location=request.location,
            experience_years=request.experience_years
        )
        return result
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        ) from exc
    except RuntimeError as exc:
        # RuntimeError from insights service indicates processing failure
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate salary recommendation: {exc}"
        ) from exc
    except Exception as exc:
        # Unexpected errors - log and return generic 500
        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating salary recommendation"
        ) from exc


@app.post("/insights/upskilling-resources", response_model=UpskillingReport)
async def get_upskilling_resources(request: UpskillingRequest = Body(...)):
    """Generate upskilling recommendations and learning path.
    
    Uses Gemini AI to identify skill gaps, find learning resources,
    and create structured learning paths with practice projects.
    
    Parameters
    ----------
    request: UpskillingRequest
        Resume ID, optional job description hash, and target role.
    
    Returns
    -------
    UpskillingReport
        Detailed skill gap analysis with learning resources and project recommendations.
    """
    try:
        insights = InsightsService()
        result = insights.get_upskilling_recommendations(
            resume_id=request.resume_id,
            job_description_hash=request.job_description_hash,
            target_role=request.target_role
        )
        return result
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        ) from exc
    except RuntimeError as exc:
        # RuntimeError from insights service indicates processing failure
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate upskilling recommendations: {exc}"
        ) from exc
    except Exception as exc:
        # Unexpected errors - log and return generic 500
        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating upskilling recommendations"
        ) from exc




