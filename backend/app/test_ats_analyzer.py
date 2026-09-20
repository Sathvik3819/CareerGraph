from app.agents.ats_analyzer import analyze_ats
from app.schemas.job import JobAnalysis
from app.schemas.resume import (
    Resume,
    ResumeHeader,
    ResumeProject,
)


job = JobAnalysis(
    job_role="Generative AI Engineer",

    required_skills=[
        "Python",
        "LangChain",
        "LangGraph",
        "FastAPI",
    ],

    preferred_skills=[
        "RAG",
        "Vector Database",
    ],

    responsibilities=[
        "Build LLM applications",
        "Develop AI agents",
    ],

    keywords=[
        "Python",
        "LangChain",
        "LangGraph",
        "FastAPI",
        "LLM",
        "RAG",
    ],
)

resume = Resume(

    header=ResumeHeader(
        name="Sathvik Chiluka",
        email="sathvik@example.com",
    ),

    summary=(
        "Computer Science student building "
        "LLM applications using Python and LangChain."
    ),

    skills=[
        "Python",
        "LangChain",
        "LangGraph",
        "FastAPI",
    ],

    projects=[
        ResumeProject(
            name="CareerGraph",

            description=(
                "Agentic resume platform using "
                "LLM and LangGraph."
            ),

            technologies=[
                "Python",
                "LangChain",
                "LangGraph",
                "FastAPI",
            ],
        )
    ],

    experience=[],

    education=[],

    certifications=[],
)

result = analyze_ats(
    resume=resume,
    job_analysis=job,
)

print("\nATS ANALYSIS")
print("=" * 40)

print(
    "Overall Score:",
    result.overall_score
)

print(
    "Required Skill Match:",
    result.required_skill_match_score
)

print(
    "Keyword Match:",
    result.keyword_match_score
)

print(
    "Section Score:",
    result.section_score
)

print(
    "\nMatched Skills:"
)

for skill in result.matched_required_skills:
    print("-", skill)

print(
    "\nMissing Skills:"
)

for skill in result.missing_required_skills:
    print("-", skill)

print(
    "\nMissing Keywords:"
)

for keyword in result.missing_keywords:
    print("-", keyword)
