"""
Insights service for salary recommendations and upskilling.
Refactored to use deep agents with structured outputs.
"""

import os
from typing import Optional
from src.storage.resume_store import (
    load_parsed_resume,
    save_salary_insights,
    save_upskilling_report,
)
from src.models.insights import SalaryRecommendation, UpskillingReport
from src.services.deep_agent_salary import SalaryResearchAgent


class InsightsService:
    """Service for generating salary and upskilling insights using deep agents."""
    
    def __init__(self):
        """Initialize with deep agent for salary research."""
        # Initialize salary research agent with structured outputs
        self.salary_agent = SalaryResearchAgent(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
        )
    
    def get_salary_recommendation(
        self,
        resume_id: str,
        job_title: Optional[str] = None,
        location: Optional[str] = None,
        experience_years: Optional[int] = None
    ) -> SalaryRecommendation:
        """
        Generate salary recommendation using deep agent with structured output.
        
        Args:
            resume_id: UUID of the resume
            job_title: Target job title (uses resume's current role if not provided)
            location: Target location (uses resume's location if not provided)
            experience_years: Years of experience (calculated from resume if not provided)
        
        Returns:
            SalaryRecommendation with structured market analysis
        
        Raises:
            RuntimeError: If resume not found or research fails
        """
        # Load resume data
        resume_data = load_parsed_resume(resume_id)
        if not resume_data:
            raise RuntimeError(f"Resume {resume_id} not found")
        
        # Extract candidate information
        skills = resume_data.get('skills', [])[:8]  # Top 8 skills
        experience = resume_data.get('experience', [])
        
        # Get location from resume if not provided
        if not location:
            contact = resume_data.get('contact', {})
            location = contact.get('location', 'United States') if contact else 'United States'
        
        # Get job title from resume if not provided
        if not job_title and experience:
            job_title = experience[0].get('job_title', 'Software Engineer')
        elif not job_title:
            job_title = 'Software Engineer'
        
        # Calculate experience years if not provided
        if not experience_years:
            experience_years = len(experience) * 2  # Heuristic: ~2 years per role
        
        # Use deep agent for salary research with structured output
        try:
            salary_recommendation = self.salary_agent.research_salary(
                job_title=job_title,
                location=location,
                experience_years=experience_years,
                skills=skills,
            )
            
            # Save salary insights to resume JSON
            save_salary_insights(
                resume_id=resume_id,
                salary_data=salary_recommendation.model_dump(mode="json"),
                job_title=job_title,
                location=location,
            )
            
            return salary_recommendation
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate salary recommendation: {e}")
    
    def get_upskilling_recommendations(
        self,
        resume_id: str,
        job_description_hash: Optional[str] = None,
        target_role: Optional[str] = None
    ) -> UpskillingReport:
        """
        Generate upskilling recommendations with structured output.
        
        Args:
            resume_id: UUID of the resume
            job_description_hash: Hash of job description for ATS score lookup (optional)
            target_role: Target role for upskilling (optional)
        
        Returns:
            UpskillingReport with structured skill gaps and learning resources
        
        Raises:
            RuntimeError: If resume not found or generation fails
        """
        # Load resume data
        resume_data = load_parsed_resume(resume_id)
        if not resume_data:
            raise RuntimeError(f"Resume {resume_id} not found")
        
        # Extract candidate information
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', [])
        
        # Get current role
        current_role = experience[0].get('job_title', 'Software Engineer') if experience else 'Software Engineer'
        
        # Use target role or current role
        if not target_role:
            target_role = current_role
        
        # Get ATS context if available
        ats_gaps = []
        ats_missing = []
        if job_description_hash:
            ats_scores = resume_data.get('ats_scores', {})
            if job_description_hash in ats_scores:
                ats_data = ats_scores[job_description_hash]
                ats_gaps = ats_data.get('gaps', [])
                ats_missing = ats_data.get('missing_keywords', [])
        
        # Create optimized prompt
        prompt = f"""Analyze skill gaps and create learning path.

Current: {current_role}
Target: {target_role}
Skills: {', '.join(skills[:10])}
{f"ATS Gaps: {', '.join(ats_gaps[:5])}" if ats_gaps else ""}
{f"Missing Keywords: {', '.join(ats_missing[:5])}" if ats_missing else ""}

Provide:
1. Identified gaps (skills to learn)
2. Target skills for {target_role}
3. Learning resources (15-20 items: videos, docs, courses)
4. Structured learning path (3-4 phases)
5. Practice projects (3-5 projects)
6. Total duration estimate
7. Expected career impact"""
        
        # Use Gemini with structured output
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.2,
                api_key=os.getenv("GEMINI_API_KEY"),
            )
            
            # Get structured output directly mapped to Pydantic model
            upskilling_report = model.with_structured_output(UpskillingReport).invoke(prompt)
            
            # Save upskilling report to resume JSON
            save_upskilling_report(
                resume_id=resume_id,
                upskilling_data=upskilling_report.model_dump(mode="json"),
                target_role=target_role,
            )
            
            return upskilling_report
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate upskilling recommendations: {e}")