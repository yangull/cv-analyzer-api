# app/analyzer.py
import json
import anthropic
from pypdf import PdfReader
from io import BytesIO
from app.models import AnalysisResult

# Initialize the client once at module level.
# It automatically reads ANTHROPIC_API_KEY from your environment.
client = anthropic.Anthropic()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Takes raw PDF bytes, returns all text content as a single string."""
    reader = PdfReader(BytesIO(pdf_bytes))
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return "\n".join(pages_text)

def analyze_cv(cv_text: str, job_description: str) -> AnalysisResult:
    """Sends CV text + job description to Claude, returns a structured AnalysisResult."""
    
    prompt = f"""You are an expert technical recruiter specializing in software engineering roles.

Analyze the following CV against the job description and return a JSON object with this exact structure:
{{
  "match_score": <integer 0-100>,
  "matched_skills": [<skills present in both CV and job description>],
  "missing_skills": [<skills the job requires that are absent from the CV>],
  "strengths": [<3-5 things the candidate does well for this role>],
  "suggestions": [<3-5 concrete actionable improvements>],
  "summary": "<one paragraph verdict on the candidate fit>"
}}

Return ONLY the JSON object. No markdown, no explanation, no code fences.

---

CV:
{cv_text}

---

Job Description:
{job_description}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_text = response.content[0].text
    raw_text = response.content[0].text
    # Strip markdown code fences if Claude added them despite instructions
    raw_text = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
  
    
    data = json.loads(raw_text)
    return AnalysisResult(**data)