"""
Configuration for deep agent prompts and settings.
Optimized for speed and accuracy with structured outputs.
"""

# Salary Research Agent Configuration
SALARY_AGENT_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.2,  # Lower for factual consistency
    "max_tokens": 4096,
    "timeout": 90,  # 90 seconds for research
    "max_search_results": 8,
}

# Salary search priority domains
SALARY_SEARCH_DOMAINS = [
    "glassdoor.com",
    "levels.fyi",
    "payscale.com",
    "linkedin.com/salary",
    "salary.com",
    "indeed.com/career",
    "bls.gov",
    "h1bdata.info",
]

# System prompt for salary research (optimized for speed)
SALARY_SYSTEM_PROMPT = """You are a Senior Compensation Analyst specializing in tech industry salary research.

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

# Upskilling Agent Configuration
UPSKILLING_AGENT_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.2,
    "max_tokens": 6144,  # Larger for resource lists
    "timeout": 120,
}
