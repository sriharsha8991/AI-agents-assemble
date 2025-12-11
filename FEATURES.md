# TalentCraft AI - Features Documentation

## 📋 Complete Feature List

### 1. Resume Processing & Structuring

**Capabilities:**
- Multiple file format support (PDF, DOCX, TXT)
- Concurrent resume upload handling
- AI-powered parsing using Google Gemini
- Structured data extraction with validation

**Data Extracted:**
- Personal Information (full name)
- Contact Information (email, phone, location, LinkedIn, GitHub, portfolio)
- Professional Summary
- Work Experience (job title, company, location, dates, responsibilities)
- Education (degree, institution, location, dates, grades)
- Skills (technical and soft skills)
- Certifications (name, issuer, date)
- Languages

**Technical Details:**
- Uses Pydantic models for data validation
- UUID-based resume identification
- JSON storage with atomic write operations
- Configurable Gemini model (default: gemini-2.5-flash)
- Configurable prompts via JSON configuration

---

### 2. ATS (Applicant Tracking System) Scoring

**Capabilities:**
- Comprehensive resume-job description compatibility analysis
- Multi-dimensional scoring system
- Intelligent caching mechanism
- Detailed feedback generation

**Scoring Components:**
- **Overall Score**: 0-100 scale
- **Section Scores**:
  - Skills Match (0-100)
  - Experience Relevance (0-100)
  - Education Fit (0-100)
  - Keyword Optimization (0-100)

**Analysis Outputs:**
- Strengths: Areas where resume aligns well
- Gaps: Weaknesses or missing elements
- Recommendations: Actionable improvement suggestions
- Missing Keywords: Critical terms from JD not in resume
- Matched Keywords: Terms present in both resume and JD
- Summary: Executive overview of evaluation

**Technical Details:**
- SHA256-based job description hashing for cache keys
- Cache stored within resume JSON files
- Configurable cache behavior (use_cache parameter)
- Atomic file updates to prevent data corruption
- Customizable scoring prompts

---

### 3. Salary Market Research

**Capabilities:**
- AI-powered compensation analysis
- Market data synthesis
- Location-based salary recommendations
- Experience-level adjustments

**Analysis Components:**
- Recommended Salary Range (min/max)
- Market Median
- 25th Percentile (lower bound)
- 75th Percentile (upper bound)
- Currency and period specification (annual/monthly/hourly)

**Factors Considered:**
- Years of experience
- Technical skills depth
- Location and cost of living
- Industry demand trends
- Company size and type

**Outputs:**
- Key Factors: List of factors influencing recommendation
- Market Trends: Current industry trends
- Sources: URLs and references for data
- Analysis Summary: Comprehensive explanation

**Technical Details:**
- Uses Gemini 2.0 Flash Exp model
- Temperature: 0.3 for consistency
- JSON-structured output
- Auto-extraction from resume if parameters not provided
- Pydantic validation with custom validators

---

### 4. Upskilling & Learning Path Generation

**Capabilities:**
- AI-driven skill gap analysis
- Learning resource curation from multiple sources
- Structured learning path creation
- Project-based learning suggestions
- Career impact assessment

**Resource Types:**
- YouTube videos and playlists
- Official documentation
- Online courses (free and paid)
- Tutorial series
- Articles and guides

**Learning Path Structure:**
- Multiple phases (Foundation → Intermediate → Advanced)
- Phase-specific skill focus
- Resource recommendations per phase
- Project suggestions per phase
- Duration estimates
- Learning objectives

**Project Suggestions Include:**
- Project title and description
- Skills practiced
- Difficulty level (beginner/intermediate/advanced)
- Estimated duration
- Key learnings expected

**Analysis Outputs:**
- Identified Gaps: Skills missing from current profile
- Target Skills: Skills to acquire
- All Resources: Complete list of 15-20+ curated resources
- Learning Path: Multi-phase structured plan
- Project Suggestions: Hands-on practice projects
- Total Duration Estimate
- Career Impact: Expected salary/career growth
- Report Summary: Executive overview

**Technical Details:**
- Integration with ATS scores for targeted recommendations
- Uses Gemini 2.0 Flash Exp model
- Temperature: 0.3 for consistency
- JSON-structured output with schema validation
- Auto-extraction from resume if parameters not provided

---

### 5. Configurable Prompt System

**File Location:** `src/config/prompts.json`

**Prompt Categories:**

#### Resume Extraction Prompts
```json
{
  "system_instruction": "Assistant behavior definition",
  "user_prompt": "Instructions for extraction task"
}
```

#### ATS Scoring Prompts
```json
{
  "system_instruction": "Expert ATS scorer persona",
  "user_prompt": "Template with {resume_json} and {job_description} placeholders"
}
```

**Benefits:**
- No code changes required for prompt updates
- Version-controlled prompt templates
- Easy A/B testing of prompts
- Template variable support
- Comprehensive error handling for missing/invalid prompts

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GEMINI_API_KEY` | Required | - | Google Gemini API authentication key |
| `GEMINI_MODEL` | Optional | `gemini-2.5-flash` | Gemini model version for resume extraction and ATS scoring |
| `DATA_DIR` | Optional | `./data/resumes/parsed` | Directory path for storing parsed resumes |
| `API_HOST` | Optional | `0.0.0.0` | Server host address (0.0.0.0 for all interfaces) |
| `API_PORT` | Optional | `8000` | Server port number |

### File-based Configuration

**Prompts Configuration:** `src/config/prompts.json`
- Resume extraction prompts
- ATS scoring prompts
- Template variables support

---

## 📊 Data Models

### Resume Model
- ExperienceItem (job_title, company, location, dates, responsibilities)
- EducationItem (degree, institution, location, dates, grade)
- CertificationItem (name, issuer, date)
- ContactInfo (email, phone, location, LinkedIn, GitHub, website)
- Resume (all above + full_name, summary, skills, languages, raw_text)

### ATS Score Model
- SectionScore (skills_match, experience_relevance, education_fit, keyword_optimization)
- ATSScore (overall_score, section_scores, strengths, gaps, recommendations, keywords, summary)

### Insights Models
- SalaryRange (min_salary, max_salary, currency, period)
- SalaryRecommendation (ranges, percentiles, factors, trends, sources, summary)
- LearningResource (title, url, type, skill, difficulty, duration, description)
- ProjectSuggestion (title, description, skills_practiced, difficulty, duration, key_learnings)
- LearningPath (phase, title, skills_focus, resources, projects, duration, objectives)
- UpskillingReport (gaps, target_skills, resources, learning_path, projects, duration, career_impact, summary)

---

## 🎯 Use Cases

### For Job Seekers
1. Upload resume → Get structured JSON
2. Score against multiple job descriptions
3. Get salary expectations for target roles
4. Identify skill gaps and get learning resources
5. Follow structured learning paths
6. Build portfolio projects

### For Recruiters
1. Upload candidate resumes in bulk
2. Score candidates against job descriptions
3. Rank candidates by ATS score
4. Identify top matches based on keywords
5. Get market salary data for positions

### For Career Coaches
1. Analyze client resumes
2. Provide data-driven feedback
3. Create personalized upskilling plans
4. Set realistic salary expectations
5. Track progress over time

---

## 🔒 Security Features

1. **API Key Management**: Environment variable-based, never hardcoded
2. **Data Isolation**: UUID-based resume storage
3. **Input Validation**: Pydantic models for all inputs/outputs
4. **File Type Validation**: Whitelist of allowed file types
5. **Atomic File Operations**: Prevents data corruption
6. **Error Handling**: Comprehensive exception handling
7. **No Sensitive Data Logging**: Careful error message design

---

## 🚀 Performance Features

1. **Intelligent Caching**: 
   - ATS scores cached by job description hash
   - Avoids redundant API calls
   - Configurable cache usage

2. **Concurrent Processing**:
   - Multiple resume uploads handled in parallel
   - Independent processing per file

3. **Efficient Storage**:
   - JSON file-based (no database overhead for MVP)
   - Atomic writes with temporary files

4. **Optimized AI Calls**:
   - Structured output reduces token usage
   - Schema validation at API level
   - Temperature tuning for consistency

---

## 📈 Future Enhancement Opportunities

### Short-term (Implemented Foundation Supports):
- ✅ Batch resume processing
- ✅ Resume data caching
- ✅ Configurable AI models
- ✅ Structured learning paths

### Medium-term (Next Steps):
- Resume comparison and ranking
- Job description parsing and structuring
- Candidate-job matching algorithms
- Interview question generation
- Progress tracking for learning paths

### Long-term (Scalability):
- Database integration (PostgreSQL/MongoDB)
- User authentication and multi-tenancy
- Real-time collaboration features
- Integration with job boards
- Mobile application
- Frontend UI/UX (React/Next.js)

---

## 📖 API Endpoints Summary

| Endpoint | Method | Purpose | Input | Output |
|----------|--------|---------|-------|--------|
| `/resumes` | POST | Upload & parse resumes | File(s) | Resume ID(s) |
| `/ats-score` | POST | Score resume vs JD | Resume ID + JD text | ATS Score |
| `/insights/salary-recommendation` | POST | Get salary data | Resume ID + optional params | Salary Analysis |
| `/insights/upskilling-resources` | POST | Get learning path | Resume ID + optional params | Upskilling Report |
| `/docs` | GET | API documentation | - | Swagger UI |
| `/redoc` | GET | API documentation | - | ReDoc UI |

---

**Last Updated:** December 10, 2025  
**Version:** 1.0.0  
**Status:** Production-ready MVP
