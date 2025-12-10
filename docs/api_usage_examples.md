# FastAPI Usage Examples - No Kestra UI Required

## Overview

You can trigger Kestra AI Agents **entirely through FastAPI** without ever touching the Kestra UI. The only thing you need to do in Kestra UI once is:
1. Deploy the flow YAML files (one-time setup)
2. Configure API keys in KV Store (GEMINI_API_KEY, TAVILY_API_KEY) OR pass as environment variables to Docker

After that, everything runs through FastAPI!

---

## How It Works

```
Your Application/Postman/curl
          ↓
    POST to FastAPI
          ↓
    KestraIntegration Service
          ↓
    Kestra Python SDK (kestrapy)
          ↓
    Kestra API (triggers workflow)
          ↓
    AI Agent executes in background
          ↓
    Results saved to resume JSON
          ↓
    GET status via FastAPI
```

---

## Complete Usage Examples

### 1. Salary Recommendation (Minimal - Auto Everything)

**Scenario**: Just provide resume ID, system auto-extracts location and calculates experience

```bash
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
  }'
```

**Postman/Thunder Client JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
}
```

**Response** (Async - returns immediately):
```json
{
  "status": "triggered",
  "execution_id": "7NqP3mK9xRzL2wF1jH5vB",
  "message": "Salary research agent triggered. Use /executions/{execution_id} to check status.",
  "flow": "salary_research_agent"
}
```

---

### 2. Salary Recommendation (Custom Location & Experience)

**Scenario**: Override location to research different market (e.g., comparing SF vs NYC)

```bash
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "job_title": "Senior AI/ML Engineer",
    "location": "San Francisco, CA",
    "experience_years": 5
  }'
```

**JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
  "job_title": "Senior AI/ML Engineer",
  "location": "San Francisco, CA",
  "experience_years": 5
}
```

---

### 3. Salary Recommendation (Synchronous - Wait for Results)

**Scenario**: Wait up to 5 minutes for agent to complete and return results

```bash
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "location": "New York, NY",
    "wait_for_completion": true
  }'
```

**JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
  "location": "New York, NY",
  "wait_for_completion": true
}
```

**Response** (after 2-3 minutes):
```json
{
  "status": "completed",
  "execution_id": "8TqW4nL0ySpM3xG2kI6wC",
  "message": "Salary research completed successfully. Check resume JSON for results."
}
```

---

### 4. Compare Salaries Across Multiple Locations

**Scenario**: Trigger multiple requests to compare salaries in different cities

```bash
# San Francisco
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "location": "San Francisco, CA"
  }'

# New York
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "location": "New York, NY"
  }'

# Seattle
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "location": "Seattle, WA"
  }'
```

All three execute in parallel, results saved to same resume JSON.

---

### 5. Upskilling Resources (Minimal)

**Scenario**: Generate upskilling plan based on most recent ATS score

```bash
curl -X POST "http://localhost:8000/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
  }'
```

**JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
}
```

---

### 6. Upskilling Resources (Specific ATS Score + Target Role)

**Scenario**: Generate upskilling plan for specific job and career goal

```bash
curl -X POST "http://localhost:8000/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "job_description_hash": "8511e3e57a9a9a88",
    "target_role": "Lead AI Architect"
  }'
```

**JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
  "job_description_hash": "8511e3e57a9a9a88",
  "target_role": "Lead AI Architect"
}
```

---

### 7. Upskilling Resources (Synchronous - Wait 10 minutes)

**Scenario**: Wait for comprehensive upskilling report (can take 3-5 minutes)

```bash
curl -X POST "http://localhost:8000/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
    "target_role": "Staff ML Engineer",
    "wait_for_completion": true
  }'
```

**JSON Body**:
```json
{
  "resume_id": "0407ed11-4f8f-4f35-89f6-a794ae2653d8",
  "target_role": "Staff ML Engineer",
  "wait_for_completion": true
}
```

---

### 8. Check Execution Status

**Scenario**: Poll for completion status of async execution

```bash
curl "http://localhost:8000/executions/7NqP3mK9xRzL2wF1jH5vB"
```

**Response** (in progress):
```json
{
  "execution_id": "7NqP3mK9xRzL2wF1jH5vB",
  "status": "RUNNING",
  "outputs": null,
  "start_date": "2025-12-09T10:30:45.123Z",
  "end_date": null
}
```

**Response** (completed):
```json
{
  "execution_id": "7NqP3mK9xRzL2wF1jH5vB",
  "status": "SUCCESS",
  "outputs": {
    "load_resume_data": {...},
    "salary_research_agent": {...},
    "save_salary_report": {...}
  },
  "start_date": "2025-12-09T10:30:45.123Z",
  "end_date": "2025-12-09T10:33:12.456Z"
}
```

---

### 9. Retrieve Results from Resume JSON

**Scenario**: Get the actual salary insights or upskilling reports

```bash
# Get salary insights
curl "http://localhost:8000/resumes/0407ed11-4f8f-4f35-89f6-a794ae2653d8" | jq '.salary_insights'

# Get upskilling reports
curl "http://localhost:8000/resumes/0407ed11-4f8f-4f35-89f6-a794ae2653d8" | jq '.upskilling_reports'

# Get latest salary insight
curl "http://localhost:8000/resumes/0407ed11-4f8f-4f35-89f6-a794ae2653d8" | jq '.salary_insights[-1]'

# Get latest upskilling report
curl "http://localhost:8000/resumes/0407ed11-4f8f-4f35-89f6-a794ae2653d8" | jq '.upskilling_reports[-1]'
```

**PowerShell**:
```powershell
# Get salary insights
$resume = Get-Content "data\resumes\parsed\0407ed11-4f8f-4f35-89f6-a794ae2653d8.json" | ConvertFrom-Json
$resume.salary_insights | ConvertTo-Json -Depth 10

# Get latest salary insight
$resume.salary_insights[-1] | ConvertTo-Json -Depth 10

# Get all upskilling reports
$resume.upskilling_reports | ConvertTo-Json -Depth 10
```

---

## Complete Workflow Example

### Scenario: New Candidate Application Processing

```bash
# Step 1: Upload resume
curl -X POST "http://localhost:8000/resumes" \
  -F "files=@resume.pdf"

# Response: {"filename": "resume.pdf", "id": "abc-123", "status": "success"}

# Step 2: Generate ATS score
curl -X POST "http://localhost:8000/ats-score" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "abc-123",
    "job_description": "Senior AI Engineer with 5+ years experience in Python, ML, AWS..."
  }'

# Step 3: Trigger salary recommendation (async)
curl -X POST "http://localhost:8000/insights/salary-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "abc-123"
  }'

# Response: {"execution_id": "exec-456", "status": "triggered"}

# Step 4: Trigger upskilling resources (async)
curl -X POST "http://localhost:8000/insights/upskilling-resources" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "abc-123",
    "target_role": "Lead AI Engineer"
  }'

# Response: {"execution_id": "exec-789", "status": "triggered"}

# Step 5: Check status (poll every 30 seconds)
curl "http://localhost:8000/executions/exec-456"
curl "http://localhost:8000/executions/exec-789"

# Step 6: Retrieve all results
curl "http://localhost:8000/resumes/abc-123"
```

---

## Python Client Example

```python
import requests
import time
import json

class TalentCraftClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def upload_resume(self, file_path):
        """Upload resume and get resume_id"""
        with open(file_path, 'rb') as f:
            files = {'files': f}
            response = requests.post(f"{self.base_url}/resumes", files=files)
            return response.json()[0]['id']
    
    def get_ats_score(self, resume_id, job_description):
        """Get ATS compatibility score"""
        payload = {
            "resume_id": resume_id,
            "job_description": job_description
        }
        response = requests.post(f"{self.base_url}/ats-score", json=payload)
        return response.json()
    
    def get_salary_recommendation(self, resume_id, location=None, wait=False):
        """Trigger salary research agent"""
        payload = {"resume_id": resume_id}
        if location:
            payload["location"] = location
        payload["wait_for_completion"] = wait
        
        response = requests.post(
            f"{self.base_url}/insights/salary-recommendation", 
            json=payload
        )
        return response.json()
    
    def get_upskilling_plan(self, resume_id, target_role=None, wait=False):
        """Trigger upskilling research agent"""
        payload = {"resume_id": resume_id}
        if target_role:
            payload["target_role"] = target_role
        payload["wait_for_completion"] = wait
        
        response = requests.post(
            f"{self.base_url}/insights/upskilling-resources", 
            json=payload
        )
        return response.json()
    
    def check_execution(self, execution_id):
        """Check execution status"""
        response = requests.get(f"{self.base_url}/executions/{execution_id}")
        return response.json()
    
    def wait_for_completion(self, execution_id, timeout=300):
        """Poll until execution completes"""
        start = time.time()
        while time.time() - start < timeout:
            status = self.check_execution(execution_id)
            if status['status'] in ['SUCCESS', 'FAILED', 'KILLED']:
                return status
            time.sleep(5)
        raise TimeoutError(f"Execution {execution_id} timed out")

# Usage
client = TalentCraftClient()

# Upload and process
resume_id = client.upload_resume("candidate_resume.pdf")
print(f"Resume uploaded: {resume_id}")

# Get salary recommendation (async)
salary_result = client.get_salary_recommendation(resume_id, location="Austin, TX")
print(f"Salary research triggered: {salary_result['execution_id']}")

# Wait for completion
final_status = client.wait_for_completion(salary_result['execution_id'])
print(f"Salary research completed: {final_status['status']}")

# Get upskilling plan (sync - waits automatically)
upskill_result = client.get_upskilling_plan(
    resume_id, 
    target_role="Senior AI Architect",
    wait=True
)
print(f"Upskilling plan ready: {upskill_result['status']}")
```

---

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

class TalentCraftClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async getSalaryRecommendation(resumeId, options = {}) {
    const payload = {
      resume_id: resumeId,
      ...options
    };
    
    const response = await axios.post(
      `${this.baseUrl}/insights/salary-recommendation`,
      payload
    );
    return response.data;
  }

  async getUpskillingPlan(resumeId, options = {}) {
    const payload = {
      resume_id: resumeId,
      ...options
    };
    
    const response = await axios.post(
      `${this.baseUrl}/insights/upskilling-resources`,
      payload
    );
    return response.data;
  }

  async checkExecution(executionId) {
    const response = await axios.get(
      `${this.baseUrl}/executions/${executionId}`
    );
    return response.data;
  }

  async waitForCompletion(executionId, timeout = 300000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const status = await this.checkExecution(executionId);
      
      if (['SUCCESS', 'FAILED', 'KILLED'].includes(status.status)) {
        return status;
      }
      
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
    
    throw new Error(`Execution ${executionId} timed out`);
  }
}

// Usage
(async () => {
  const client = new TalentCraftClient();
  
  // Get salary for multiple locations
  const cities = ['San Francisco, CA', 'New York, NY', 'Austin, TX'];
  const resumeId = '0407ed11-4f8f-4f35-89f6-a794ae2653d8';
  
  const executions = await Promise.all(
    cities.map(city => 
      client.getSalaryRecommendation(resumeId, { location: city })
    )
  );
  
  console.log('All salary researches triggered:', executions);
  
  // Wait for all to complete
  const results = await Promise.all(
    executions.map(exec => client.waitForCompletion(exec.execution_id))
  );
  
  console.log('All completed:', results);
})();
```

---

## Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "TalentCraft AI - Insights API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "resume_id",
      "value": "0407ed11-4f8f-4f35-89f6-a794ae2653d8"
    }
  ],
  "item": [
    {
      "name": "Salary Recommendation - Auto",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "url": "{{base_url}}/insights/salary-recommendation",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"resume_id\": \"{{resume_id}}\"\n}"
        }
      }
    },
    {
      "name": "Salary Recommendation - Custom",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/insights/salary-recommendation",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"resume_id\": \"{{resume_id}}\",\n  \"location\": \"San Francisco, CA\",\n  \"experience_years\": 5\n}"
        }
      }
    },
    {
      "name": "Upskilling Resources",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/insights/upskilling-resources",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"resume_id\": \"{{resume_id}}\",\n  \"target_role\": \"Lead AI Architect\"\n}"
        }
      }
    },
    {
      "name": "Check Execution Status",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/executions/{{execution_id}}"
      }
    }
  ]
}
```

---

## Environment Variables

Make sure these are set before running FastAPI:

```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
KESTRA_HOST=http://localhost:8080
KESTRA_USERNAME=root@root.com
KESTRA_PASSWORD=Root!1234
```

---

## One-Time Kestra UI Setup (Required)

You only need to do this ONCE:

### 1. Deploy Flows

1. Open http://localhost:8080
2. Go to **Flows** → **Create**
3. Copy/paste content from `kestra_flows/salary_research_agent.yaml`
4. Click **Save**
5. Repeat for `kestra_flows/upskilling_research_agent.yaml`

### 2. Configure API Keys (KV Store)

**Option A: Using Kestra UI KV Store**
1. Go to **Namespaces** → **hackoo.insights**
2. Click **KV Store** tab
3. Add:
   - Key: `GEMINI_API_KEY`, Value: Your Gemini API key
   - Key: `TAVILY_API_KEY`, Value: Your Tavily API key

**Option B: Using Docker Environment Variables (Production-Ready)**

When running Kestra with Docker, pass environment variables:

```bash
docker run -d \\
  --name kestra \\
  -p 8080:8080 \\
  -e GEMINI_API_KEY="your-gemini-key" \\
  -e TAVILY_API_KEY="your-tavily-key" \\
  -v /path/to/hackoo/data:/data \\
  kestra/kestra:latest
```

The flows use `{{ kv('KEY_NAME') }}` which automatically reads from both KV Store and environment variables.

### 3. Done! Never Touch UI Again

From now on, trigger everything via FastAPI endpoints. The Kestra UI is just for viewing execution logs if needed.

---

## Summary

✅ **No Kestra UI needed for triggering** - everything via FastAPI  
✅ **Async by default** - get execution_id immediately  
✅ **Sync mode available** - wait for completion if needed  
✅ **Poll for status** - check execution progress anytime  
✅ **Results in resume JSON** - easily retrievable  
✅ **Fully programmable** - integrate with any app/frontend  

Just call FastAPI endpoints with simple JSON payloads! 🚀
