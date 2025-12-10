
#  TalentCraft AI
This repository will act as primary proof of work for Hackathon on AI Agents assemble by @WEMAKEDEVS

Hackathon Timeline: 8 Dec - 14 Dec (2025)
### *AI-powered Skill Growth & Smarter Hiring Platform*

TalentCraft AI is a two-sided intelligent platform designed to help **applicants grow** and **recruiters hire smarter**.
The system uses modern AI capabilities to analyze resumes, summarize job descriptions, generate personalized learning paths, and recommend the best candidates for a role — all while delivering a clean, intuitive UI/UX.

This repository contains the initial setup and structure for the hackathon submission for **AI Agents Assemble – WeMakeDevs**.

---

## 🚀 **NEW: Kestra AI Agents Integration**

This project now includes **autonomous market research agents** powered by [Kestra](https://kestra.io) that provide:

1. **Salary Recommendation Agent**: Market analysis using real compensation data (Glassdoor, Levels.fyi, LinkedIn) to recommend optimal salary ranges based on skills, experience, and location
2. **Upskilling Resources Agent**: AI-powered learning path generator that identifies skill gaps and curates 15-20+ resources (YouTube tutorials, documentation, courses) with structured learning paths and project suggestions

Both agents use **Gemini 2.0 Flash** with **TavilyWebSearch** for autonomous web research and structured JSON output.

👉 **[Complete Setup Guide & Documentation](#kestra-ai-agents-setup)**

---

#  Project Overview

TalentCraft AI provides:

###  **For Applicants**

* Resume, Job description upload 
* AI-powered insights
* Skill extraction & gap analysis
* Personalized learning path generation
* Micro-project suggestions
* Progress tracking dashboard

###  **For Recruiters**

* Upload job descriptions (JD)
* AI-powered JD summarization
* Candidate–JD skill fit analysis
* Candidate ranking & insights
* Automated interview workflow triggers

This system prioritizes **clean UI**, **modern UX**, and **realistic AI workflows**, keeping the user journey simple and powerful.

---

#  Technologies (Planned)

This project will incorporate the sponsor tools required by the hackathon:

### 🟦 **Vercel**

Frontend deployment for a clean, fast, and reliable user experience.

### 🟧 **Oumi**

Used for:

* Resume/JD understanding
* Skill gap reasoning
* Learning path generation
* RL fine-tuning (as required for Iron Intelligence Award)

### 🟪 **Kestra** ✅ **IMPLEMENTED**

**Autonomous AI Agent orchestration** for:

* ✅ **Salary Market Research Agent**: Analyzes compensation data from Glassdoor, Levels.fyi, LinkedIn Salary, Payscale using Gemini 2.0 Flash + TavilyWebSearch
* ✅ **Upskilling Resources Agent**: Searches YouTube, documentation, courses for skill gaps; generates structured learning paths with 15-20+ resources
* 🔜 JD summarization workflows
* 🔜 Decision-making workflows for candidate ranking
* 🔜 Interview scheduling automation
* 🔜 Weekly learning path updates

**Agent Architecture**: Kestra AI Agents with LLM (Gemini 2.0 Flash Exp) + TavilyWebSearch tool + JSON schema validation + persistent results

### 🟨 **Cline CLI**

Developer automation tool (separate from main app) to demonstrate:

* Autonomous code generation
* Workflow automation
* New capabilities on top of Cline
  (Required for Infinity Build Award)

### 🟩 **CodeRabbit**

Used for PR reviews and ensuring:

* Clean code
* Documentation hygiene
* Open-source best practices

---

## 🧠 Kestra AI Agents Setup

### What is Kestra?

**Kestra** is an open-source, event-driven orchestration platform (25.9k GitHub stars) that enables autonomous AI-powered workflows using declarative YAML configuration.

We use Kestra's **AI Agents** feature to build market research agents that:
- Make autonomous decisions about when to use web search tools
- Gather real-time compensation data and learning resources
- Output structured JSON validated against Pydantic schemas
- Persist results in resume JSON files

### Architecture

```
FastAPI (Port 8000)
  ├─ POST /resumes (resume upload)
  ├─ POST /ats-score (ATS scoring)
  ├─ POST /insights/salary-recommendation (NEW)
  ├─ POST /insights/upskilling-resources (NEW)
  └─ GET /executions/{execution_id} (NEW)
         │
         │ Triggers via KestraIntegration
         ▼
Kestra Platform (Port 8080)
  ├─ salary_research_agent
  │    ├─ Load resume data
  │    ├─ AI Agent (Gemini 2.0 + TavilyWebSearch)
  │    └─ Save salary insights
  │
  └─ upskilling_research_agent
       ├─ Load ATS scores
       ├─ AI Agent (Gemini 2.0 + TavilyWebSearch)
       └─ Save upskilling report
```

### Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Start Kestra

**Note:** Set `DATA_DIR` to your local data directory path before running:

```bash
# Set your data directory (adjust path for your system)
export DATA_DIR=/path/to/your/data
# Or on Windows PowerShell: $env:DATA_DIR = "D:\path\to\your\data"

# Run Kestra with the mounted data directory
docker run --pull=always --rm -it -p 8080:8080 --user=root \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ${DATA_DIR}:/data \
  kestra/kestra:latest server local
```

Access UI: http://localhost:8080

#### 3. Deploy Kestra Flows

1. Go to http://localhost:8080
2. Navigate to **Flows** → **Create**
3. Copy content from `kestra_flows/salary_research_agent.yaml`
4. Click **Save**
5. Repeat for `kestra_flows/upskilling_research_agent.yaml`

#### 4. Configure API Keys (KV Store)

Kestra Open Source uses KV (Key-Value) store for configuration instead of Secrets (Enterprise-only).

**Option A: Using Kestra UI**
1. Go to **Namespaces** → **hackoo.insights**
2. Click **KV Store** tab
3. Add:
   - Key: `GEMINI_API_KEY`, Value: Your Gemini API key
   - Key: `TAVILY_API_KEY`, Value: Get free key from [tavily.com](https://tavily.com) (1000 searches/month free)

**Option B: Using Docker Environment Variables (Recommended for deployment)**

When running Kestra with Docker, pass environment variables that will be accessible via `{{ kv() }}`:

**Note:** Replace `/path/to/data` with your actual host directory path (e.g., `$PWD/data` or absolute path).

```bash
docker run -d \
  --name kestra \
  -p 8080:8080 \
  -e GEMINI_API_KEY=your_gemini_key_here \
  -e TAVILY_API_KEY=your_tavily_key_here \
  -v /path/to/data:/data \
  kestra/kestra:latest
```

#### 5. Set Environment Variables

Create `.env`:

> **⚠️ SECURITY WARNING:** The values below are examples only and must NOT be used in production. Always use secure, unique credentials. Store secrets in a secure vault or environment management system, rotate credentials regularly, and never commit real credentials to version control.

```bash
GEMINI_API_KEY=your_gemini_key_here
KESTRA_HOST=http://localhost:8080
KESTRA_USERNAME=root@root.com
KESTRA_PASSWORD=Root!1234
```

#### 6. Run FastAPI

```bash
uvicorn src.api_main:app --reload --port 8000
```

### Usage Examples

**Get Salary Recommendation (Auto-Location):**

```bash
# Minimal request - auto-extracts location from resume
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
  }'
```

**Get Salary Recommendation (Custom Location):**

```bash
# Override location for targeted research
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "job_title": "Senior AI/ML Engineer",
    "location": "San Francisco, CA",
    "experience_years": 5,
    "wait_for_completion": false
  }'
```

**Get Upskilling Resources (Sync):**

```bash
curl -X POST "http://localhost:8000/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "job_description_hash": "8511e3e57a9a9a88",
    "target_role": "Lead AI Architect",
    "wait_for_completion": true
  }'
```

**Check Execution Status:**

```bash
curl "http://localhost:8000/executions/{execution_id}"
```

### Sample Output

**Salary Insights:**
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
    "2 years production AI/ML experience",
    "RAG and LLM orchestration expertise"
  ],
  "market_trends": [
    "Generative AI roles commanding 15-25% premium"
  ],
  "sources": [
    "https://www.levels.fyi/t/software-engineer",
    "https://www.glassdoor.com/Salaries/ai-ml-engineer-salary"
  ]
}
```

**Upskilling Report:**
```json
{
  "identified_gaps": ["NoSQL", "Kubernetes", "Terraform"],
  "all_resources": [
    {
      "title": "MongoDB Crash Course",
      "url": "https://youtube.com/watch?v=ofme2o29ngU",
      "type": "youtube_video",
      "skill": "NoSQL",
      "difficulty": "beginner",
      "duration": "1 hour"
    }
    // ... 15-20 more resources
  ],
  "learning_path": [
    {
      "phase": 1,
      "title": "Foundation - Database & Governance",
      "skills_focus": ["NoSQL", "Data Governance"],
      "duration": "2-3 weeks",
      "projects": [
        {
          "title": "Build E-Commerce Catalog with MongoDB",
          "skills_practiced": ["MongoDB", "Data Modeling"]
        }
      ]
    }
  ],
  "estimated_total_duration": "8-12 weeks",
  "career_impact": "Expected salary impact: +15-25%"
}
```

### Documentation

- **Complete API Documentation**: `docs/insights_api_documentation.md`
- **Kestra AI Agents Docs**: https://kestra.io/docs/ai-tools/ai-agents
- **Tavily API**: https://tavily.com

