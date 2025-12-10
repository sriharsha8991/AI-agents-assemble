"""
Direct insights service for salary recommendations and upskilling without Kestra.
Uses Gemini AI with function calling and web search.
"""

import json
from typing import Optional, Dict, Any
from src.services.gemini_client import GeminiClient
from src.storage.resume_store import load_parsed_resume
from src.models.insights import SalaryRecommendation, UpskillingReport


class InsightsService:
    """Direct service for generating salary and upskilling insights using Gemini AI."""
    
    def __init__(self):
        """Initialize with Gemini client."""
        self.gemini = GeminiClient()
    
    def get_salary_recommendation(
        self,
        resume_id: str,
        job_title: Optional[str] = None,
        location: Optional[str] = None,
        experience_years: Optional[int] = None
    ) -> SalaryRecommendation:
        """
        Generate salary recommendation based on resume and market research.
        
        Args:
            resume_id: UUID of the resume
            job_title: Target job title (uses resume's current role if not provided)
            location: Target location (uses resume's location if not provided)
            experience_years: Years of experience (calculated from resume if not provided)
        
        Returns:
            SalaryRecommendation with market analysis
        
        Raises:
            RuntimeError: If resume not found or generation fails
        """
        # Load resume data
        resume_data = load_parsed_resume(resume_id)
        if not resume_data:
            raise RuntimeError(f"Resume {resume_id} not found")
        
        # Extract candidate information
        skills = resume_data.get('skills', [])[:10]  # Top 10 skills
        experience = resume_data.get('experience', [])
        full_name = resume_data.get('full_name', 'Candidate')
        
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
        
        # Create prompt for Gemini
        prompt = f"""
You are an expert compensation analyst and market research specialist.

Candidate Profile:
- Name: {full_name}
- Skills: {', '.join(skills)}
- Experience: {experience_years} years
- Recent Roles: {', '.join([exp.get('job_title', '') for exp in experience[:3]])}

Target Position:
- Job Title: {job_title}
- Location: {location}

Conduct a comprehensive salary market analysis and provide a detailed recommendation.

Research current compensation data from multiple reliable sources including:
- Glassdoor, Payscale, Levels.fyi, LinkedIn Salary
- Industry reports and compensation surveys
- Job postings with salary ranges

Analyze multiple data points to determine:
- Market median salary
- 25th percentile (lower bound)
- 75th percentile (upper bound)
- Recommended range based on candidate's profile

Consider key factors:
- Years of experience
- Technical skills depth (AI/ML, cloud, specific frameworks)
- Location and cost of living
- Industry demand
- Company size and type

Identify market trends:
- Emerging skills commanding premiums
- Industry growth areas
- Remote work impact on compensation

Return a JSON object with this exact structure:
{{
    "recommended_range": {{
        "min_salary": <number>,
        "max_salary": <number>,
        "currency": "USD",
        "period": "annual"
    }},
    "market_median": <number>,
    "percentile_25": <number>,
    "percentile_75": <number>,
    "key_factors": [<list of strings>],
    "market_trends": [<list of strings>],
    "sources": [<list of URLs>],
    "analysis_summary": "<comprehensive text summary>"
}}

All salary figures should be in USD annual.
"""
        
        # Generate response using Gemini with web search
        try:
            response = self.gemini.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config={
                    'temperature': 0.3,
                    'response_mime_type': 'application/json'
                }
            )
            
            # Parse JSON response
            result_text = response.text
            salary_data = json.loads(result_text)
            
            # Create and return SalaryRecommendation object
            return SalaryRecommendation(**salary_data)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse salary recommendation response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate salary recommendation: {e}")    
    def get_upskilling_recommendations(
        self,
        resume_id: str,
        job_description_hash: Optional[str] = None,
        target_role: Optional[str] = None
    ) -> UpskillingReport:
        """
        Generate upskilling recommendations and learning path.
        
        Args:
            resume_id: UUID of the resume
            job_description_hash: Hash of job description for ATS score lookup (optional)
            target_role: Target role for upskilling (optional)
        
        Returns:
            UpskillingReport with skill gaps and learning resources
        
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
        full_name = resume_data.get('full_name', 'Candidate')
        
        # Get current role
        current_role = experience[0].get('job_title', 'Software Engineer') if experience else 'Software Engineer'
        
        # Use target role or current role
        if not target_role:
            target_role = current_role
        
        # Try to get ATS score if job_description_hash is provided
        ats_context = ""
        if job_description_hash:
            ats_scores = resume_data.get('ats_scores', {})
            if job_description_hash in ats_scores:
                ats_data = ats_scores[job_description_hash]
                ats_context = f"""

ATS Analysis for Target Role:
- Overall ATS Score: {ats_data.get('overall_score', 'N/A')}/100
- Identified Gaps: {', '.join(ats_data.get('gaps', []))}
- Missing Keywords: {', '.join(ats_data.get('missing_keywords', []))}
- Matched Keywords: {', '.join(ats_data.get('matched_keywords', []))}
- ATS Recommendations: {', '.join(ats_data.get('recommendations', []))}

Please prioritize addressing the identified gaps and missing keywords in your upskilling recommendations.
"""
        
        # Create prompt for Gemini
        prompt = f"""
You are an expert career development advisor and technical skills analyst.

Candidate Profile:
- Name: {full_name}
- Current Skills: {', '.join(skills)}
- Current Role: {current_role}
- Target Role: {target_role}
{ats_context}
Analyze the skill gap between current skills and target role requirements.

Research and provide:
1. Skills Assessment:
   - Current strengths
   - Skills gaps to address
   - Emerging skills for the target role

2. Learning Resources:
   - YouTube tutorials and channels
   - Official documentation
   - Online courses (free and paid)
   - Books and articles

3. Learning Path:
   - Ordered sequence of topics to learn
   - Estimated time for each topic
   - Difficulty level

4. Practice Projects:
   - Real-world projects to build
   - Complexity level
   - Skills demonstrated

Return a JSON object with this exact structure:
{{
    "skill_gaps": [
        {{
            "skill": "<skill name>",
            "importance": "<high|medium|low>",
            "current_level": "<beginner|intermediate|advanced|none>",
            "target_level": "<intermediate|advanced|expert>"
        }}
    ],
    "learning_resources": [
        {{
            "title": "<resource title>",
            "type": "<youtube|documentation|course|book|article>",
            "url": "<URL>",
            "description": "<brief description>",
            "difficulty": "<beginner|intermediate|advanced>",
            "estimated_hours": <number>
        }}
    ],
    "learning_path": [
        {{
            "topic": "<topic name>",
            "order": <number>,
            "duration_weeks": <number>,
            "resources": [<list of resource titles from above>]
        }}
    ],
    "practice_projects": [
        {{
            "title": "<project title>",
            "description": "<what to build>",
            "skills_practiced": [<list of skills>],
            "complexity": "<simple|intermediate|advanced>",
            "estimated_hours": <number>
        }}
    ],
    "summary": "<comprehensive analysis and recommendations>"
}}
"""
        
        # Generate response using Gemini
        try:
            response = self.gemini.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config={
                    'temperature': 0.3,
                    'response_mime_type': 'application/json'
                }
            )
            
            # Parse JSON response
            result_text = response.text
            upskilling_data = json.loads(result_text)
            
            # Create and return UpskillingReport object
            return UpskillingReport(**upskilling_data)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse upskilling recommendation response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate upskilling recommendations: {e}")