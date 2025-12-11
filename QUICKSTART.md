# Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### 1. Clone Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Gemini API Key
GEMINI_API_KEY=<your-gemini-api-key>

# Optional: Custom Configuration
GEMINI_MODEL=gemini-2.5-flash
DATA_DIR=./data/resumes/parsed
API_HOST=0.0.0.0
API_PORT=8000
```

> **Note:** Replace `<your-gemini-api-key>` with your actual API key. Never commit this file to version control.

### 4. Start FastAPI Server

```bash
# Development mode with auto-reload
uvicorn src.api_main:app --reload --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000}
```

### 5. Test the API

```bash
# Upload a resume (replace with your actual file path)
curl -X POST "http://localhost:${API_PORT:-8000}/resumes" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/your/resume.pdf"

# Get salary recommendation (use the resume_id from upload response)
curl -X POST "http://localhost:${API_PORT:-8000}/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "<your-resume-uuid>",
    "job_title": "Senior Software Engineer",
    "location": "San Francisco, CA",
    "experience_years": 5
  }'

# Get upskilling recommendations
curl -X POST "http://localhost:${API_PORT:-8000}/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "<your-resume-uuid>",
    "target_role": "AI/ML Engineer"
  }'
```

## 🔑 Get Your API Key

### Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key and add it to your `.env` file

## ✅ What's Running?

✅ FastAPI server with auto-reload enabled  
✅ AI-powered resume processing  
✅ ATS scoring with intelligent caching  
✅ Salary market research using Gemini AI  
✅ Upskilling recommendations with learning paths

## 📚 Next Steps

- **API Docs:** http://localhost:${API_PORT:-8000}/docs
- **ReDoc:** http://localhost:${API_PORT:-8000}/redoc
- **Full Documentation:** See `README.md`
- **API Examples:** See `docs/api_usage_examples.md`

## 🔍 Troubleshooting

**Issue:** "GEMINI_API_KEY environment variable is not set"

**Solution:** Ensure your `.env` file exists and contains the API key:
```bash
# Check if .env file exists
cat .env

# Or on Windows PowerShell
Get-Content .env
```

**Issue:** Server won't start or module not found errors

**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

**Issue:** Resume upload fails

**Solution:** Check file format (must be PDF, DOCX, or TXT) and file size limits.

## 💡 Pro Tips

- Use the interactive API docs at `/docs` endpoint for easy testing
- Set `use_cache=false` in ATS scoring to force re-evaluation
- Check stored resumes in `${DATA_DIR:-./data/resumes/parsed}/` directory
- Review prompt templates in `src/config/prompts.json` for customization

## 🔐 Security Reminders

- ⚠️ Never commit `.env` file to version control
- ⚠️ Keep your API keys secure and rotate them regularly
- ⚠️ Use environment-specific configurations for different deployments
