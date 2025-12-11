"""
Deep agent implementation for salary market research using Tavily and Gemini.
Provides structured outputs via Pydantic models and optimized prompts.
"""

import os
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from src.models.insights import SalaryRecommendation


class SalaryResearchAgent:
    """Deep agent for comprehensive salary market research."""
    
    def __init__(self, gemini_api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        """
        Initialize salary research agent.
        
        Args:
            gemini_api_key: Google Gemini API key (uses env var if not provided)
            tavily_api_key: Tavily API key (uses env var if not provided)
        """
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")
        
        if not self.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment")
        if not self.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY not found in environment")
        
        # Initialize Tavily client
        self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
        
        # Create search tool
        self._create_search_tool()
        
        # Initialize Gemini model with structured output
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.2,  # Lower for factual consistency
            max_tokens=4096,
            api_key=self.gemini_api_key,
        )
        
        # Create the deep agent
        self.agent = create_deep_agent(
            model=self.model,
            tools=[self.salary_search],
            system_prompt=self._get_system_prompt(),
        )
    
    def _create_search_tool(self):
        """Create specialized salary search tool."""
        def salary_search(query: str, max_results: int = 8) -> Dict[str, Any]:
            """
            Search salary databases and compensation platforms.
            
            Args:
                query: Search query (e.g., "Senior Software Engineer salary NYC 2025")
                max_results: Number of results to return
            
            Returns:
                Search results with salary data
            """
            # Priority domains for salary data
            include_domains = [
                "glassdoor.com",
                "levels.fyi",
                "payscale.com",
                "linkedin.com",
                "salary.com",
                "indeed.com",
                "bls.gov",
            ]
            
            try:
                results = self.tavily_client.search(
                    query=query,
                    max_results=max_results,
                    include_domains=include_domains,
                    topic="general",
                    include_raw_content=True,
                )
                return results
            except Exception as e:
                return {"error": str(e), "results": []}
        
        self.salary_search = salary_search
    
    def _get_system_prompt(self) -> str:
        """Get optimized system prompt for salary research."""
        return """You are a Senior Compensation Analyst specializing in tech industry salary research.

**Your Task:** Provide data-driven salary recommendations using market research.

**Research Process:**
1. Search salary databases (Glassdoor, Levels.fyi, Payscale, LinkedIn)
2. Gather data for role, location, and experience level
3. Calculate percentiles (25th, median, 75th)
4. Identify key factors affecting compensation
5. Note current market trends

**Output Requirements:**
Return JSON with:
- recommended_range: {min_salary, max_salary, currency, period}
- market_median: median salary value
- percentile_25: 25th percentile
- percentile_75: 75th percentile  
- key_factors: list of 5-7 key factors
- market_trends: list of 3-5 current trends
- sources: list of URLs used
- analysis_summary: 2-3 sentence summary

**Quality Standards:**
✓ Use 3+ authoritative sources
✓ Specify USD annual unless stated otherwise
✓ Account for location cost of living
✓ Include skill premiums (AI/ML, cloud, etc.)
✓ Be realistic and data-driven"""
    
    def research_salary(
        self,
        job_title: str,
        location: str,
        experience_years: int,
        skills: List[str],
    ) -> SalaryRecommendation:
        """
        Conduct salary research and return structured recommendation.
        
        Args:
            job_title: Target job title
            location: Target location
            experience_years: Years of experience
            skills: List of key skills
        
        Returns:
            SalaryRecommendation with structured market data
        
        Raises:
            RuntimeError: If research fails
        """
        # Create concise research query
        query = f"""Research salary for:
Role: {job_title}
Location: {location}
Experience: {experience_years} years
Key Skills: {', '.join(skills[:6])}

Provide comprehensive market analysis with salary ranges, percentiles, factors, trends, and sources."""
        
        try:
            # Invoke agent
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            # Extract response
            agent_response = result["messages"][-1].content
            
            # Use Gemini's structured output to parse into Pydantic model
            structured_response = self.model.with_structured_output(SalaryRecommendation).invoke(
                f"Parse this salary research into the required format:\n\n{agent_response}"
            )
            
            return structured_response
            
        except Exception as e:
            raise RuntimeError(f"Salary research failed: {e}")
