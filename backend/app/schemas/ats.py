from pydantic import BaseModel, Field


class ATSAnalysis(BaseModel):
    overall_score: int = Field(
        ge=0,
        le=100
    )

    required_skill_match_score: int = Field(
        ge=0,
        le=100
    )

    preferred_skill_match_score: int = Field(
        ge=0,
        le=100
    )

    keyword_match_score: int = Field(
        ge=0,
        le=100
    )

    section_score: int = Field(
        ge=0,
        le=100
    )

    matched_required_skills: list[str] = Field(
        default_factory=list
    )

    missing_required_skills: list[str] = Field(
        default_factory=list
    )

    matched_preferred_skills: list[str] = Field(
        default_factory=list
    )

    missing_preferred_skills: list[str] = Field(
        default_factory=list
    )

    matched_keywords: list[str] = Field(
        default_factory=list
    )

    missing_keywords: list[str] = Field(
        default_factory=list
    )

    missing_sections: list[str] = Field(
        default_factory=list
    )
