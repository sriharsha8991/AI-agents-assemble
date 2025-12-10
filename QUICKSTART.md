# Quick Start - Open Source Setup

## ⚡ Fast Setup (5 minutes)

### 1. Start Kestra with API Keys

```bash
docker run -d \
  --name kestra \
  -p 8080:8080 \
  -e GEMINI_API_KEY="YOUR_GEMINI_KEY_HERE" \
  -e TAVILY_API_KEY="YOUR_TAVILY_KEY_HERE" \
  -v /d/Sriharsha/personal/hackoo/data:/data \
  kestra/kestra:latest
```

### 2. Deploy Flows

1. Open http://localhost:8080
2. Go to **Flows** → **Create**
3. Copy/paste from:
   - `kestra_flows/salary_research_agent.yaml`
   - `kestra_flows/upskilling_research_agent.yaml`
4. Click **Save** for each

### 3. Install Python Dependencies

```bash
cd d:\Sriharsha\personal\hackoo
pip install -r requirements.txt
```

### 4. Start FastAPI

```bash
uvicorn src.api_main:app --reload --port 8000
```

### 5. Test It!

```bash
# Salary recommendation
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "job_title": "Senior ML Engineer"
  }'

# Upskilling plan
curl -X POST "http://localhost:8000/insights/upskilling-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "target_role": "AI/ML Engineer"
  }'
```

## 🔑 Get Free API Keys

### Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key (starts with `AIzaSy...`)

### Tavily API Key
1. Go to https://tavily.com
2. Sign up (free - 1000 searches/month)
3. Copy API key from dashboard (starts with `tvly-...`)

## ✅ What Just Happened?

✅ Kestra running with API keys as environment variables  
✅ AI Agent flows deployed (salary + upskilling)  
✅ FastAPI server ready to trigger workflows  
✅ No Enterprise license needed - pure Open Source!

## 📚 Next Steps

- **API Docs:** http://localhost:8000/docs
- **Kestra UI:** http://localhost:8080
- **Full Guide:** See `docs/api_usage_examples.md`
- **Migration Info:** See `docs/kv_store_migration.md`

## 🔍 Troubleshooting

**Issue:** "API key not found" error in Kestra execution

**Solution:** Check environment variables are passed correctly:
```bash
docker exec kestra env | grep API_KEY
```

**Issue:** FastAPI can't connect to Kestra

**Solution:** Ensure Kestra is running and accessible:
```bash
curl http://localhost:8080/api/v1/health
```

## 💡 Pro Tips

- Use `.env` file for local development
- Use Kubernetes Secrets for production
- Check Kestra execution logs: UI → Executions → Click execution ID
- All AI Agent outputs saved to resume JSON files
