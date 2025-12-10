## Resume Structuring Service

This service provides FastAPI endpoints to upload resume files, extract structured data using Google Gemini, and score resumes against job descriptions using ATS criteria.

### Endpoints

#### 1. `POST /resumes` - Upload and Parse Resumes

- **Body**: multipart form-data with field `files` (PDF, DOCX, or TXT).
- **Response on success**:
  ```json
  [
    {
      "filename": "resume.pdf",
      "id": "<uuid>",
      "status": "success"
    }
  ]
  ```
- The structured JSON is stored on disk under `data/resumes/parsed/<uuid>.json`.

#### 2. `POST /ats-score` - Score Resume Against Job Description

- **Body**: JSON with the following fields:
  ```json
  {
    "resume_id": "uuid-of-parsed-resume",
    "job_description": "Full job description text...",
    "use_cache": true  // Optional, defaults to true
  }
  ```
- **Caching**: ATS scores are automatically cached in the resume JSON file. Subsequent requests with the same `resume_id` and `job_description` will return the cached result instantly without calling the Gemini API. Set `use_cache: false` to force re-evaluation.
  
- **Response on success**:
  ```json
  {
    "overall_score": 85,
    "section_scores": {
      "skills_match": 90,
      "experience_relevance": 85,
      "education_fit": 80,
      "keyword_optimization": 85
    },
    "strengths": ["Strong technical skills match", "Relevant experience"],
    "gaps": ["Missing certification X"],
    "recommendations": ["Add keywords: cloud, DevOps"],
    "missing_keywords": ["cloud computing", "DevOps"],
    "matched_keywords": ["Python", "JavaScript", "API"],
    "summary": "Strong candidate with good technical alignment..."
  }
  ```

### Architecture

#### Prompts Configuration (`src/config/prompts.json`)

All LLM prompts are centralized in a JSON configuration file for easy maintenance:

- `resume_extraction`: Prompts for extracting structured resume data
- `ats_scoring`: Prompts for scoring resumes against job descriptions

This separation allows you to update prompts without changing code.

#### Services

- **`GeminiClient`** (`src/services/gemini_client.py`): Multi-purpose Gemini client
  - `extract_resume(file_path, schema)`: Extracts structured data from resume files
  - `score_resume_ats(resume_data, job_description, schema)`: Scores resume against job description
  - Loads prompts from `src/config/prompts.json`

- **`ATSScorer`** (`src/services/ats_scorer.py`): High-level ATS scoring service
  - Fetches stored resume JSON by ID
  - **Checks cache before calling Gemini API** - avoids redundant API calls for same resume-job combinations
  - Uses GeminiClient to perform ATS evaluation when cache miss occurs
  - Automatically caches results in the resume JSON file
  - Returns structured `ATSScore` model

- **Storage** (`src/storage/resume_store.py`): Resume and ATS score persistence
  - `save_parsed_resume()`: Saves extracted resume data
  - `load_parsed_resume()`: Retrieves resume by ID
  - `get_cached_ats_score()`: Checks for cached ATS score
  - `save_ats_score()`: Stores ATS score in resume JSON under `ats_scores` field
  - Uses SHA-256 hash of job description as cache key

#### Models

- **`Resume`** (`src/models/resume.py`): Structured resume schema
- **`ATSScore`** (`src/models/ats_score.py`): ATS scoring result schema with:
  - Overall score (0-100)
  - Section scores (skills, experience, education, keywords)
  - Strengths, gaps, recommendations
  - Missing and matched keywords
  - Summary of overall assessment

### Environment Variables

- `GEMINI_API_KEY`: API key from Google AI Studio used by the Gemini client.

### Install & Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set the API key (PowerShell example):

```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
```

3. Run the FastAPI app from the project root:

```bash
uvicorn src.api_main:app --reload
```

### Usage Examples

#### Upload Resume

```bash
curl -X POST "http://localhost:8000/resumes" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/resume.pdf"
```

**Response:**
```json
[
  {
    "filename": "resume.pdf",
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "success"
  }
]
```

#### Score Resume Against Job Description

```bash
curl -X POST "http://localhost:8000/ats-score" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "job_description": "We are looking for a Senior Python Developer with 5+ years of experience in FastAPI, REST APIs, and cloud technologies. Must have experience with AWS, Docker, and CI/CD pipelines..."
  }'
```

**First Request**: Calls Gemini API, caches result in resume JSON  
**Subsequent Requests**: Returns cached result instantly (no API call)

To force re-evaluation (ignore cache):
```bash
curl -X POST "http://localhost:8000/ats-score" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "job_description": "...",
    "use_cache": false
  }'
```

**Response:**
```json
{
  "overall_score": 85,
  "section_scores": {
    "skills_match": 90,
    "experience_relevance": 85,
    "education_fit": 80,
    "keyword_optimization": 85
  },
  "strengths": [
    "Strong Python and FastAPI experience",
    "Demonstrated REST API development skills"
  ],
  "gaps": [
    "No explicit mention of AWS experience",
    "Missing Docker/containerization details"
  ],
  "recommendations": [
    "Add AWS certifications if available",
    "Highlight Docker and CI/CD experience in projects section"
  ],
  "missing_keywords": ["AWS", "Docker", "CI/CD"],
  "matched_keywords": ["Python", "FastAPI", "REST API"],
  "summary": "Strong technical candidate with excellent Python skills..."
}
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`