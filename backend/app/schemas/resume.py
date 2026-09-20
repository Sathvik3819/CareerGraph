from pydantic import BaseModel, Field


class ResumeHeader(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    portfolio_url: str | None = None


class ResumeProject(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    github_url: str | None = None
    live_url: str | None = None


class ResumeExperience(BaseModel):
    company: str
    role: str
    duration: str
    description: list[str] = Field(default_factory=list)


class ResumeEducation(BaseModel):
    institution: str
    degree: str
    duration: str
    grade: str | None = None


class Resume(BaseModel):
    header: ResumeHeader
    summary: str

    skills: list[str] = Field(
        default_factory=list
    )

    projects: list[ResumeProject] = Field(
        default_factory=list
    )

    experience: list[ResumeExperience] = Field(
        default_factory=list
    )

    education: list[ResumeEducation] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )