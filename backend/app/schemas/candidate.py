from pydantic import BaseModel, Field


class CandidateAnalysis(BaseModel):
    technical_skills: list[str] = Field(
        description="Technical skills possessed by the candidate."
    )

    soft_skills: list[str] = Field(
        description="Soft skills explicitly supported by the candidate information."
    )

    strongest_projects: list[str] = Field(
        description="Projects that appear most valuable based on the candidate information."
    )

    experience_highlights: list[str] = Field(
        description="Important experience or achievement highlights."
    )

    certifications: list[str] = Field(
        description="Certifications mentioned by the candidate."
    )

    missing_information: list[str] = Field(
        description="Important candidate information that appears to be missing."
    )