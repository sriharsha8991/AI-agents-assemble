from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class SalaryRange(BaseModel):
    """Salary range with currency information."""
    
    min_salary: float = Field(
        ...,
        description="Minimum salary in the specified currency.",
    )
    max_salary: float = Field(
        ...,
        description="Maximum salary in the specified currency.",
    )
    currency: str = Field(
        default="USD",
        description="Currency code (e.g., USD, EUR, INR).",
    )
    period: str = Field(
        default="annual",
        description="Salary period (annual, monthly, hourly).",
    )
    @model_validator(mode='after')
    def validate_salary_range(self) -> 'SalaryRange':
        if self.min_salary > self.max_salary:
            raise ValueError(f"min_salary ({self.min_salary}) cannot exceed max_salary ({self.max_salary})")
        return self


class SalaryRecommendation(BaseModel):
    """Market-based salary recommendation for a candidate."""
    
    recommended_range: SalaryRange = Field(
        ...,
        description="Recommended salary range based on market analysis.",
    )
    market_median: float = Field(
        ...,
        description="Market median salary for similar profiles.",
    )
    percentile_25: float = Field(
        ...,
        description="25th percentile salary (lower bound).",
    )
    percentile_75: float = Field(
        ...,
        description="75th percentile salary (upper bound).",
    )
    key_factors: List[str] = Field(
        default_factory=list,
        description="Key factors influencing salary recommendation (experience, skills, location, etc.).",
    )
    market_trends: List[str] = Field(
        default_factory=list,
        description="Current market trends affecting compensation.",
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Data sources used for market analysis (URLs, reports).",
    )
    analysis_summary: str = Field(
        ...,
        description="Comprehensive summary of salary analysis.",
    )


class LearningResource(BaseModel):
    """Individual learning resource (video, course, documentation)."""
    
    title: str = Field(
        ...,
        description="Title of the learning resource.",
    )
    url: str = Field(
        ...,
        description="URL to the resource.",
    )
    type: str = Field(
        ...,
        description="Type of resource (youtube_video, playlist, documentation, course, tutorial).",
    )
    skill: str = Field(
        ...,
        description="Primary skill this resource addresses.",
    )
    difficulty: Optional[str] = Field(
        default=None,
        description="Difficulty level (beginner, intermediate, advanced).",
    )
    duration: Optional[str] = Field(
        default=None,
        description="Estimated duration/length (e.g., '2 hours', '10-week course').",
    )
    description: Optional[str] = Field(
        default=None,
        description="Brief description of what the resource covers.",
    )


class ProjectSuggestion(BaseModel):
    """Practical project suggestion for skill building."""
    
    title: str = Field(
        ...,
        description="Project title.",
    )
    description: str = Field(
        ...,
        description="Detailed project description.",
    )
    skills_practiced: List[str] = Field(
        default_factory=list,
        description="Skills that will be practiced through this project.",
    )
    difficulty: str = Field(
        ...,
        description="Project difficulty level (beginner, intermediate, advanced).",
    )
    estimated_duration: str = Field(
        ...,
        description="Estimated time to complete (e.g., '1 week', '2-3 weeks').",
    )
    key_learnings: List[str] = Field(
        default_factory=list,
        description="Key learnings expected from completing this project.",
    )


class LearningPath(BaseModel):
    """Structured learning path for skill development."""
    
    phase: int = Field(
        ...,
        description="Phase number in the learning path (1-based).",
    )
    title: str = Field(
        ...,
        description="Phase title (e.g., 'Foundation', 'Intermediate', 'Advanced').",
    )
    skills_focus: List[str] = Field(
        default_factory=list,
        description="Skills to focus on in this phase.",
    )
    resources: List[LearningResource] = Field(
        default_factory=list,
        description="Recommended resources for this phase.",
    )
    projects: List[ProjectSuggestion] = Field(
        default_factory=list,
        description="Suggested projects for this phase.",
    )
    duration: str = Field(
        ...,
        description="Estimated duration for this phase.",
    )
    objectives: List[str] = Field(
        default_factory=list,
        description="Learning objectives for this phase.",
    )
    
    @field_validator("phase")
    @classmethod
    def validate_phase(cls, v: int) -> int:
        """Validate that phase is a positive 1-based integer."""
        if v <= 0:
            raise ValueError(
                f"Phase must be a positive 1-based integer (greater than 0), got {v}. "
                "Learning path phases should start at 1 and increment sequentially."
            )
        return v


class UpskillingReport(BaseModel):
    """Comprehensive upskilling report with resources and learning path."""
    
    identified_gaps: List[str] = Field(
        default_factory=list,
        description="Skills gaps identified from ATS analysis.",
    )
    target_skills: List[str] = Field(
        default_factory=list,
        description="Target skills to acquire for better job opportunities.",
    )
    all_resources: List[LearningResource] = Field(
        default_factory=list,
        description="All recommended learning resources.",
    )
    learning_path: List[LearningPath] = Field(
        default_factory=list,
        description="Structured learning path with phases.",
    )
    project_suggestions: List[ProjectSuggestion] = Field(
        default_factory=list,
        description="All recommended project suggestions.",
    )
    estimated_total_duration: str = Field(
        ...,
        description="Total estimated time to complete the learning path.",
    )
    career_impact: str = Field(
        ...,
        description="Expected career impact after completing the learning path.",
    )
    report_summary: str = Field(
        ...,
        description="Executive summary of the upskilling plan.",
    )
