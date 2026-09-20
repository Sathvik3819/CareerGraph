from typing import TypedDict

from app.schemas.ats import ATSAnalysis
from app.schemas.candidate import CandidateAnalysis
from app.schemas.job import JobAnalysis
from app.schemas.resume import Resume
from app.schemas.review import ResumeReview


class ResumeState(TypedDict, total=False):
    candidate_profile: str
    job_description: str

    candidate_analysis: CandidateAnalysis
    job_analysis: JobAnalysis

    resume: Resume
    review: ResumeReview
    ats_analysis: ATSAnalysis

    iteration: int
    status: str
    pdf_path: str
    template: str