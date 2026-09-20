import re

from app.schemas.ats import ATSAnalysis
from app.schemas.job import JobAnalysis
from app.schemas.resume import Resume
from app.utils.skill_normalizer import normalize_skill


def normalize_text(text: str) -> str:
    """
    Normalize text so keyword comparisons
    are case-insensitive and punctuation-independent.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_keyword(
    text: str,
    keyword: str
) -> bool:

    normalized_text = normalize_text(text)
    normalized_keyword = normalize_text(keyword)

    if not normalized_keyword:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(normalized_keyword)
        + r"(?![a-z0-9])"
    )

    return bool(
        re.search(
            pattern,
            normalized_text
        )
    )


def build_resume_text(resume: Resume) -> str:

    parts = []

    parts.append(
        resume.header.name
    )

    parts.append(
        resume.summary
    )

    parts.extend(
        resume.skills
    )

    for project in resume.projects:

        parts.append(project.name)

        parts.append(
            project.description
        )

        parts.extend(
            project.technologies
        )

    for experience in resume.experience:

        parts.append(
            experience.company
        )

        parts.append(
            experience.role
        )

        parts.append(
            experience.duration
        )

        parts.extend(
            experience.description
        )

    for education in resume.education:

        parts.append(
            education.institution
        )

        parts.append(
            education.degree
        )

        parts.append(
            education.duration
        )

        if education.grade:
            parts.append(
                education.grade
            )

    parts.extend(
        resume.certifications
    )

    return "\n".join(parts)


def get_resume_skills(resume: Resume) -> set[str]:
    skills = []

    skills.extend(resume.skills)

    for project in resume.projects:
        skills.extend(project.technologies)

    return {
        normalize_skill(skill)
        for skill in skills
        if skill and skill.strip()
    }


def contains_skill(resume_text: str, skill: str) -> bool:
    normalized_resume = normalize_text(resume_text)
    canonical_skill = normalize_skill(skill)

    if not canonical_skill:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(canonical_skill)
        + r"(?![a-z0-9])"
    )

    return bool(re.search(pattern, normalized_resume))


def analyze_ats(
    resume: Resume,
    job_analysis: JobAnalysis
) -> ATSAnalysis:

    resume_text = build_resume_text(
        resume
    )
    resume_skills = get_resume_skills(resume)

    # --------------------------------
    # Required skill matching
    # --------------------------------

    matched_required_skills = []
    missing_required_skills = []

    for skill in job_analysis.required_skills:
        canonical_skill = normalize_skill(skill)

        if canonical_skill in resume_skills:
            matched_required_skills.append(skill)
        else:
            missing_required_skills.append(skill)

    if job_analysis.required_skills:
        required_skill_score = round(
            len(matched_required_skills)
            / len(job_analysis.required_skills) * 100
        )
    else:
        required_skill_score = 100

    # --------------------------------
    # Preferred skill matching
    # --------------------------------

    matched_preferred_skills = []
    missing_preferred_skills = []

    for skill in job_analysis.preferred_skills:
        canonical_skill = normalize_skill(skill)

        if canonical_skill in resume_skills:
            matched_preferred_skills.append(skill)
        else:
            missing_preferred_skills.append(skill)

    if job_analysis.preferred_skills:
        preferred_skill_score = round(
            len(matched_preferred_skills)
            / len(job_analysis.preferred_skills) * 100
        )
    else:
        preferred_skill_score = 100

    # --------------------------------
    # Keyword matching
    # --------------------------------

    matched_keywords = []
    missing_keywords = []

    for keyword in job_analysis.keywords:
        normalized_keyword = normalize_skill(keyword)

        if contains_keyword(
            resume_text,
            normalized_keyword or keyword
        ):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    if job_analysis.keywords:
        keyword_score = round(
            len(matched_keywords)
            / len(job_analysis.keywords) * 100
        )
    else:
        keyword_score = 100

    # --------------------------------
    # Section checks
    # --------------------------------

    missing_sections = []

    if not resume.summary.strip():
        missing_sections.append("Professional Summary")

    if not resume.skills:
        missing_sections.append("Skills")

    if not resume.projects:
        missing_sections.append("Projects")

    if not resume.education:
        missing_sections.append("Education")

    section_total = 4
    section_score = round(
        (section_total - len(missing_sections)) / section_total * 100
    )

    # --------------------------------
    # Overall score
    # --------------------------------

    overall_score = round(
        required_skill_score * 0.45
        + keyword_score * 0.25
        + preferred_skill_score * 0.10
        + section_score * 0.20
    )

    return ATSAnalysis(
        overall_score=overall_score,
        required_skill_match_score=required_skill_score,
        preferred_skill_match_score=preferred_skill_score,
        keyword_match_score=keyword_score,
        section_score=section_score,
        matched_required_skills=matched_required_skills,
        missing_required_skills=missing_required_skills,
        matched_preferred_skills=matched_preferred_skills,
        missing_preferred_skills=missing_preferred_skills,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        missing_sections=missing_sections,
    )
