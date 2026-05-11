# app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# UploadFile — represents the uploaded file
# File — marks the parameter as a file upload field
# Form — marks the parameter as a form text field
# HTTPException — lets us return proper error responses with status codes

from app.analyzer import extract_text_from_pdf, analyze_cv  # our Claude logic
from app.models import AnalysisResult                        # our response shape

app = FastAPI(
    title="CV Analyzer API",
    description="Upload a CV (PDF) and a job description to get a Claude-powered gap analysis.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Quick endpoint to confirm the service is running."""
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze(
    cv_file: UploadFile = File(..., description="Your CV as a PDF file"),
    job_description: str = Form(..., description="Paste the job description here")
):
    """
    Accepts a CV PDF and a job description.
    Returns a structured Claude-powered match analysis.
    """

    # Validate the uploaded file is actually a PDF before doing anything else.
    # content_type is sent by the client in the request headers.
    if cv_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read the raw bytes from the uploaded file.
    # We use await because file reading is an async I/O operation in FastAPI.
    pdf_bytes = await cv_file.read()

    # Extract readable text from the PDF bytes
    cv_text = extract_text_from_pdf(pdf_bytes)

    # Guard against scanned PDFs that have no text layer —
    # pypdf can't extract text from images, only from text-based PDFs.
    if not cv_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from PDF. Make sure it's a text-based PDF, not a scanned image."
        )

    # Run the Claude analysis and return the structured result.
    # FastAPI automatically validates it against AnalysisResult before sending.
    result = analyze_cv(cv_text, job_description)
    return result