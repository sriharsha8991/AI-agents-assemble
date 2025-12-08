## Resume Structuring Service

This service provides a single FastAPI endpoint to upload a resume file and store a structured JSON representation using Google Gemini.

### Endpoint

- `POST /resumes`
	- Body: multipart form-data with field `file` (PDF, DOCX, or TXT).
	- Response on success:
		- `{"id": "<uuid>", "status": "success"}`
	- The structured JSON is stored on disk under `data/resumes/parsed/<uuid>.json`.

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

4. Test the endpoint (example with `curl`):

```bash
curl -X POST "http://localhost:8000/resumes" \
	-H "accept: application/json" \
	-H "Content-Type: multipart/form-data" \
	-F "file=@/path/to/your_resume.pdf"
```

On success, the service returns an `id` and stores the parsed resume JSON on disk for later processing.
