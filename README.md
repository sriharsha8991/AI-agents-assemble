


#  TalentCraft AI

### *AI-powered Skill Growth & Smarter Hiring Platform*

TalentCraft AI is a two-sided intelligent platform designed to help **applicants grow** and **recruiters hire smarter**.
The system uses modern AI capabilities to analyze resumes, summarize job descriptions, generate personalized learning paths, and recommend the best candidates for a role.

---

## ✨ **Features**

### **Implemented Features:**

#### 1. **Resume Processing & Structuring**
- Upload multiple resume files (PDF, DOCX, TXT)
- AI-powered resume parsing using configurable Gemini models
- Structured JSON extraction (contact info, skills, experience, education, certifications, languages)
- Persistent storage with UUID-based identification
- Configurable data storage directory

#### 2. **ATS (Applicant Tracking System) Scoring**
- Resume-to-job-description compatibility scoring (0-100 scale)
- Detailed section scores:
  - Skills match
  - Experience relevance
  - Education fit
  - Keyword optimization
- Strengths and gaps analysis
- Missing/matched keywords identification
- Actionable recommendations for improvement
- Intelligent caching (avoids re-scoring same resume-JD combinations)

#### 3. **Salary Market Research**
- AI-powered salary recommendations
- Market analysis with median, percentile data (25th, 75th)
- Recommended salary ranges based on:
  - Skills and experience
  - Location and market trends
  - Industry demand
- Key factors analysis and source citations

#### 4. **Upskilling & Learning Path Generation**
- AI-driven skill gap identification
- Learning resource curation (YouTube, documentation, courses)
- Structured multi-phase learning paths
- Hands-on project suggestions with difficulty levels
- Career impact analysis
- Integration with ATS scores for targeted skill development

#### 5. **Configurable Prompt System**
- JSON-based prompt configuration (`src/config/prompts.json`)
- Separate prompts for resume extraction and ATS scoring
- Easy customization without code changes

---

## 🏗️ **Architecture**

### Technology Stack

- **Backend**: FastAPI (Python)
- **AI Models**: Google Gemini (configurable model version)
- **Data Storage**: JSON file-based storage
- **API Standards**: RESTful API with OpenAPI/Swagger documentation

### System Components

```
FastAPI Server (Configurable Port)
  ├─ POST /resumes (resume upload & processing)
  ├─ POST /ats-score (ATS scoring with caching)
  ├─ POST /insights/salary-recommendation (salary analysis)
  └─ POST /insights/upskilling-resources (learning path generation)
         │
         │ Uses
         ▼
Gemini AI Services
  ├─ Resume Extraction (gemini-2.5-flash or configurable)
  ├─ ATS Scoring
  ├─ Salary Market Research (gemini-2.0-flash-exp or configurable)
  └─ Upskilling Recommendations
         │
         │ Stores
         ▼
JSON Storage (Configurable Directory)
  └─ data/resumes/parsed/{uuid}.json
       ├─ Resume data
       ├─ ATS scores (cached)
       └─ Insights (future)

```

---

## 🚀 **Quick Start**

### Prerequisites

- Python 3.8+
- pip package manager
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Installation

#### 1. Clone Repository

```bash
git clone <repository-url>
cd <project-directory>
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Gemini API Key
GEMINI_API_KEY=<your-gemini-api-key>

# Optional: Custom Gemini Model (default: gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash

# Optional: Data Storage Directory (default: ./data/resumes/parsed)
DATA_DIR=<absolute-path-to-data-directory>

# Optional: Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

> **⚠️ SECURITY WARNING:** Never commit `.env` file or real API keys to version control. Use environment management systems for production deployments.

#### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn src.api_main:app --reload --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000}
```

#### 5. Access API Documentation

- **Interactive Docs**: http://localhost:${API_PORT}/docs
- **ReDoc**: http://localhost:${API_PORT}/redoc

---

## 📝 **Configuration**

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ | - | Google Gemini API key for AI processing |
| `GEMINI_MODEL` | ❌ | `gemini-2.5-flash` | Gemini model version to use |
| `DATA_DIR` | ❌ | `./data/resumes/parsed` | Directory for storing parsed resumes |
| `API_HOST` | ❌ | `0.0.0.0` | Server host address |
| `API_PORT` | ❌ | `8000` | Server port number |

### Prompt Configuration

Customize AI behavior by editing `src/config/prompts.json`:

```json
{
  "resume_extraction": {
    "system_instruction": "<your-custom-instruction>",
    "user_prompt": "<your-custom-prompt>"
  },
  "ats_scoring": {
    "system_instruction": "<your-custom-instruction>",
    "user_prompt": "<template-with-{resume_json}-and-{job_description}>"
  }
}
```

---

## 🔌 **API Usage Examples**

### 1. Upload Resume

```bash
curl -X POST "http://localhost:${API_PORT}/resumes" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/resume.pdf"
```

**Response:**
```json
[
  {
    "filename": "resume.pdf",
    "id": "uuid-here",
    "status": "success"
  }
]
```

### 2. Score Resume (ATS)

```bash
curl -X POST "http://localhost:${API_PORT}/ats-score" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "<resume-uuid>",
    "job_description": "<job-description-text>",
    "use_cache": true
  }'
```

### 3. Get Salary Recommendation

```bash
curl -X POST "http://localhost:${API_PORT}/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "<resume-uuid>",
    "job_title": "Senior Software Engineer",
    "location": "San Francisco, CA",
    "experience_years": 5
  }'
```

### 4. Get Upskilling Resources

```bash
curl -X POST "http://localhost:${API_PORT}/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "<resume-uuid>",
    "job_description_hash": "<optional-hash>",
    "target_role": "AI/ML Engineer"
  }'
```

---

## 📊 **Response Examples**
---

## 📊 **Response Examples**

### Salary Recommendation Response

```json
{
  "recommended_range": {
    "min_salary": 110000,
    "max_salary": 145000,
    "currency": "USD",
    "period": "annual"
  },
  "market_median": 125000,
  "percentile_25": 105000,
  "percentile_75": 150000,
  "key_factors": [
    "X years production experience",
    "Relevant technology stack expertise"
  ],
  "market_trends": [
    "Industry-specific trends and premiums"
  ],
  "sources": [
    "https://www.levels.fyi/...",
    "https://www.glassdoor.com/..."
  ],
  "analysis_summary": "Comprehensive market analysis..."
}
```

### Upskilling Report Response

```json
{
  "identified_gaps": ["Skill1", "Skill2", "Skill3"],
  "target_skills": ["TargetSkill1", "TargetSkill2"],
  "all_resources": [
    {
      "title": "Resource Title",
      "url": "https://example.com",
      "type": "youtube_video",
      "skill": "Skill1",
      "difficulty": "beginner",
      "duration": "2 hours",
      "description": "Resource description"
    }
  ],
  "learning_path": [
    {
      "phase": 1,
      "title": "Foundation Phase",
      "skills_focus": ["Skill1", "Skill2"],
      "duration": "2-3 weeks",
      "objectives": ["Objective1", "Objective2"],
      "resources": [],
      "projects": []
    }
  ],
  "project_suggestions": [
    {
      "title": "Project Title",
      "description": "Build something practical",
      "skills_practiced": ["Skill1", "Skill2"],
      "difficulty": "intermediate",
      "estimated_duration": "1-2 weeks",
      "key_learnings": ["Learning1", "Learning2"]
    }
  ],
  "estimated_total_duration": "8-12 weeks",
  "career_impact": "Expected salary impact and career growth",
  "report_summary": "Executive summary of upskilling plan"
}
```

### ATS Score Response

```json
{
  "overall_score": 78,
  "section_scores": {
    "skills_match": 85,
    "experience_relevance": 75,
    "education_fit": 70,
    "keyword_optimization": 80
  },
  "strengths": [
    "Strong technical skills alignment",
    "Relevant industry experience"
  ],
  "gaps": [
    "Missing specific certification",
    "Limited experience in required technology"
  ],
  "recommendations": [
    "Add more project descriptions",
    "Include quantified achievements"
  ],
  "missing_keywords": ["keyword1", "keyword2"],
  "matched_keywords": ["keyword3", "keyword4"],
  "summary": "Overall assessment summary"
}
```

---

## 🗂️ **Project Structure**

```
project-root/
├── .env                          # Environment variables (not in git)
├── .gitignore
├── requirements.txt              # Python dependencies
├── README.md
├── QUICKSTART.md
├── data/
│   └── resumes/
│       └── parsed/               # Parsed resume JSON storage
│           └── {uuid}.json
├── docs/
│   ├── api_usage_examples.md
│   └── inital_doc.md
└── src/
    ├── __init__.py
    ├── api_main.py               # FastAPI application
    ├── config/
    │   └── prompts.json          # AI prompt templates
    ├── models/
    │   ├── resume.py             # Resume data model
    │   ├── ats_score.py          # ATS scoring model
    │   └── insights.py           # Salary & upskilling models
    ├── services/
    │   ├── gemini_client.py      # Gemini AI client wrapper
    │   ├── ats_scorer.py         # ATS scoring service
    │   └── insights_service.py   # Salary & upskilling service
    └── storage/
        └── resume_store.py       # JSON file storage operations
```

---

## 🧪 **Development**

### Running in Development Mode

```bash
# With auto-reload
uvicorn src.api_main:app --reload --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000}
```

### Testing API Endpoints

Use the interactive API documentation at `http://localhost:${API_PORT}/docs` to test endpoints with a user-friendly interface.

### Customizing Prompts

Edit `src/config/prompts.json` to modify AI behavior:

- **resume_extraction**: Controls how resumes are parsed
- **ats_scoring**: Controls ATS scoring criteria and analysis

---

## 🔐 **Security Best Practices**

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive configuration
3. **Rotate API keys** regularly
4. **Use `.gitignore`** to exclude `.env` and sensitive files
5. **Implement rate limiting** in production
6. **Validate all user inputs** before processing
7. **Use HTTPS** in production deployments

---

## 🚢 **Deployment**

### Environment Setup

For production deployments, set environment variables through your hosting platform:

- **Vercel/Netlify**: Use platform environment variable settings
- **AWS/GCP/Azure**: Use secrets management services
- **Docker**: Pass environment variables via `-e` flag or docker-compose
- **Kubernetes**: Use ConfigMaps and Secrets

### Docker Deployment (Example)

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use environment variables
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

CMD ["sh", "-c", "uvicorn src.api_main:app --host $API_HOST --port $API_PORT"]
```

```bash
# Build and run
docker build -t talentcraft-ai .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=<your-key> \
  -e GEMINI_MODEL=<model-name> \
  -v $(pwd)/data:/app/data \
  talentcraft-ai
```

---

## 📚 **Documentation**

- **API Documentation**: Available at `/docs` endpoint (Swagger UI)
- **ReDoc**: Available at `/redoc` endpoint
- **Usage Examples**: See `docs/api_usage_examples.md`
- **Quick Start Guide**: See `QUICKSTART.md`

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests if applicable
5. Update documentation
6. Submit a pull request

---

## 📄 **License**

This project is part of the AI Agents Assemble Hackathon by WeMakeDevs.

---

## 🙏 **Acknowledgments**

- **WeMakeDevs** for organizing the AI Agents Assemble Hackathon
- **Google Gemini** for powerful AI capabilities
- **FastAPI** for excellent Python web framework
- **Pydantic** for robust data validation

---

## 📞 **Support**

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review API examples in `/docs`

---

**Built with ❤️ for the AI Agents Assemble Hackathon**