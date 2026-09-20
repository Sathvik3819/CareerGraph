from pydantic import BaseModel , Field

class JobAnalysis(BaseModel):
    job_role: str = Field(
        description="The job title or role mentioned in the job description."
    )

    required_skills: list[str] = Field(
        description="Skills explicitly required for the job."
    )

    preferred_skills: list[str] = Field(
        description="Skills mentioned as preferred, optional, or nice-to-have."
    )

    responsibilities: list[str] = Field(
        description="Main responsibilities associated with the job."
    )

    keywords: list[str] = Field(
        description="Important technical and domain keywords from the job description."
    )