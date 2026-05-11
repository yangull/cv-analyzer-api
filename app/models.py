# app/models.py
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    suggestions: list[str]
    summary: str