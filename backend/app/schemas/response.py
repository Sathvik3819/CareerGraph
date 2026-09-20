from datetime import datetime

from pydantic import BaseModel

from app.schemas.ats import ATSAnalysis
from app.schemas.resume import Resume
from app.schemas.review import ResumeReview


class ResumeGenerationResponse(BaseModel):
    resume_id: str

    status: str

    iterations: int

    resume: Resume

    review: ResumeReview

    ats_analysis: ATSAnalysis

    pdf_path: str | None = None


class ResumeHistoryItem(BaseModel):
    id: str
    candidate_name: str
    job_role: str
    template: str
    iterations: int
    ats_score: int
    review_score: int
    decision: str
    created_at: datetime


class ResumeHistoryResponse(BaseModel):
    resumes: list[ResumeHistoryItem]


class ResumeDetailResponse(BaseModel):
    id: str
    candidate_name: str
    job_role: str
    job_description: str
    template: str
    iterations: int
    candidate_data: dict
    resume: Resume
    review: ResumeReview
    ats_analysis: ATSAnalysis
    created_at: datetime