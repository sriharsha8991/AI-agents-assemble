from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SectionScore(BaseModel):
    skills_match: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Score for skills alignment with job requirements (0-100).",
    )
    experience_relevance: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Score for experience relevance to the role (0-100).",
    )
    education_fit: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Score for education match with job requirements (0-100).",
    )
    keyword_optimization: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Score for keyword density and ATS optimization (0-100).",
    )


class ATSScore(BaseModel):
    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall ATS compatibility score (0-100).",
    )
    section_scores: SectionScore = Field(
        ...,
        description="Detailed section-wise scoring breakdown.",
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="List of strengths where resume aligns with job requirements.",
    )
    gaps: List[str] = Field(
        default_factory=list,
        description="List of gaps or weaknesses in the resume.",
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations to improve ATS score.",
    )
    missing_keywords: List[str] = Field(
        default_factory=list,
        description="Critical keywords from job description missing in resume.",
    )
    matched_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords that are present in both resume and job description.",
    )
    summary: Optional[str] = Field(
        default=None,
        description="Brief summary of the ATS evaluation.",
    )
