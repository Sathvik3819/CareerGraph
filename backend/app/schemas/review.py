from typing import Literal

from pydantic import BaseModel, Field


class ResumeReview(BaseModel):

    score: int = Field(
        ge=0,
        le=100,
        description="Overall resume score from 0 to 100."
    )

    decision: Literal["APPROVED", "REVISE"] = Field(
        description="Whether the resume is good enough or needs revision."
    )

    job_match_score: int = Field(
        ge=0,
        le=100,
        description="How well the resume matches the target job."
    )

    ats_score: int = Field(
        ge=0,
        le=100,
        description="Estimated ATS compatibility score."
    )

    factual_consistency_score: int = Field(
        ge=0,
        le=100,
        description="How well the resume stays consistent with candidate information."
    )

    missing_keywords: list[str] = Field(
        default_factory=list,
        description="Important job keywords missing from the resume."
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Strong aspects of the generated resume."
    )

    issues: list[str] = Field(
        default_factory=list,
        description="Problems that should be fixed."
    )

    suggestions: list[str] = Field(
        default_factory=list,
        description="Specific improvements that should be made."
    )