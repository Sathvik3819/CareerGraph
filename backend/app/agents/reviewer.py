from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.schemas.review import ResumeReview

load_dotenv()

endpoint = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="text-generation",
    temperature=0.1,
    do_sample=False,
)
llm = ChatHuggingFace(llm=endpoint)

parser = PydanticOutputParser(pydantic_object=ResumeReview)

prompt_template = PromptTemplate(
    template="""
You are a strict technical resume reviewer.

Your job is to evaluate a generated resume against:

1. The candidate's actual information
2. The target job description
3. The structured job analysis

Evaluate the resume for:
- Job description alignment
- Technical skill relevance
- Project relevance
- ATS compatibility
- Keyword coverage
- Factual consistency
- Resume quality

IMPORTANT:
- Never assume the candidate has a skill that is not supported by the candidate information.
- Identify unsupported claims.
- Do not reward invented metrics.
- Do not require a skill simply because it is common in the industry.
- Only compare the resume against the provided job description.
- Be strict and objective.
- Provide actionable feedback.

Approval rule:
Approve the resume only if it is sufficiently aligned with the job and does not
contain significant factual problems.

{format_instructions}

Candidate Information:

{candidate_profile}

Candidate Analysis:

{candidate_analysis}

Job Description:

{job_description}

Job Analysis:

{job_analysis}

Generated Resume:

{resume}

Return ONLY the JSON object. No extra text, no markdown fences.
""",
    input_variables=["candidate_profile", "candidate_analysis", "job_description", "job_analysis", "resume"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | llm | parser


def review_resume(
    candidate_profile: str,
    candidate_analysis,
    job_description: str,
    job_analysis,
    resume
) -> ResumeReview:

    result = chain.invoke({
        "candidate_profile": candidate_profile,
        "candidate_analysis": candidate_analysis,
        "job_description": job_description,
        "job_analysis": job_analysis,
        "resume": resume,
    })

    return result