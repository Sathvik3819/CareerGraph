from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.resume import Resume


class PersonalInfoRequest(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    github: str | None = None
    linkedin: str | None = None
    portfolio: str | None = None


class EducationRequest(BaseModel):
    institution: str
    degree: str
    duration: str
    grade: str | None = None


class ProjectRequest(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    github_url: str | None = None
    live_url: str | None = None


class ExperienceRequest(BaseModel):
    company: str
    role: str
    duration: str
    description: str


class ResumeGenerationRequest(BaseModel):

    personal: PersonalInfoRequest

    education: list[EducationRequest] = Field(
        default_factory=list
    )

    skills: list[str] = Field(
        default_factory=list
    )

    projects: list[ProjectRequest] = Field(
        default_factory=list
    )

    experience: list[ExperienceRequest] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )

    job_role: str

    job_description: str

    template: Literal["modern", "classic", "minimal"] = "modern"


class PDFGenerationRequest(BaseModel):
    resume: Resume
    template: Literal["modern", "classic", "minimal"] = "modern"