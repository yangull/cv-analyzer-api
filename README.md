# CV Analyzer API

A FastAPI service that accepts a CV (PDF) and a job description, sends both to Claude AI, and returns a structured gap analysis with match score, missing skills, strengths, and actionable suggestions.

## What it does

- Accepts a CV as a PDF upload and a job description as text
- Extracts text from the PDF using pypdf
- Sends both to Claude (claude-haiku-4-5) for analysis
- Returns structured JSON: match score, matched skills, missing skills, strengths, suggestions, summary

## Tech stack

- FastAPI
- Claude AI (Anthropic API)
- pypdf
- Pydantic
- Uvicorn

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs to test via Swagger UI.

## Requirements

- Python 3.10+
- ANTHROPIC_API_KEY set as environment variable