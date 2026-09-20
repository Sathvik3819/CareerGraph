from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.schemas.resume import Resume

load_dotenv()

endpoint = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="text-generation",
    temperature=0.2,
    do_sample=False,
)
llm = ChatHuggingFace(llm=endpoint)

parser = PydanticOutputParser(pydantic_object=Resume)


def create_resume(
    candidate_profile: str,
    candidate_analysis,
    job_analysis,
    existing_resume=None,
    review=None
) -> Resume:

    # ---------------------------------------------------------
    # MODE 1: CREATE A NEW RESUME
    # ---------------------------------------------------------
    if existing_resume is None:

        prompt_template = PromptTemplate(
            template="""
You are a professional technical resume writer.

Create a job-tailored resume using ONLY the information provided by the candidate.

IMPORTANT RULES:

1. Never invent skills.
2. Never invent work experience.
3. Never invent companies.
4. Never invent certifications.
5. Never invent achievements.
6. Never invent metrics or percentages.
7. Never invent GitHub or portfolio URLs.
8. Do not claim that the candidate knows a technology unless
   it is present in the candidate information.
9. Prioritize skills and projects relevant to the target job.
10. Keep the resume concise and suitable for a one-page resume.
11. Rewrite descriptions professionally while preserving their factual meaning.
12. Do not include unsupported information.

HEADER INFORMATION RULES:
- Preserve the candidate's name exactly.
- Include email only if provided.
- Include phone only if provided.
- Include location only if provided.
- Include GitHub URL only if provided.
- Include LinkedIn URL only if provided.
- Include portfolio URL only if provided.
- Never invent contact information.
- Never modify or fabricate URLs.

{format_instructions}

TARGET JOB ANALYSIS:
{job_analysis}

CANDIDATE ANALYSIS:
{candidate_analysis}

ORIGINAL CANDIDATE INFORMATION:
{candidate_profile}

Return ONLY the JSON object. No extra text, no markdown fences.
""",
            input_variables=["job_analysis", "candidate_analysis", "candidate_profile"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt_template | llm | parser
        result = chain.invoke({
            "job_analysis": job_analysis,
            "candidate_analysis": candidate_analysis,
            "candidate_profile": candidate_profile,
        })

    # ---------------------------------------------------------
    # MODE 2: IMPROVE AN EXISTING RESUME
    # ---------------------------------------------------------
    else:

        prompt_template = PromptTemplate(
            template="""
You are a professional technical resume improvement agent.

An existing resume has already been created and reviewed.

Your task is to IMPROVE the existing resume based on the reviewer's feedback.

Do NOT create an entirely new resume.

Make only the changes necessary to address the reviewer's feedback while
preserving the factual information already present in the resume and candidate profile.

IMPORTANT RULES:

1. Never invent skills.
2. Never invent work experience.
3. Never invent companies.
4. Never invent certifications.
5. Never invent achievements.
6. Never invent metrics or percentages.
7. Never invent GitHub, LinkedIn, portfolio, or other URLs.
8. Never add a technology unless it is supported by the candidate information.
9. Never add an achievement unless it is supported by the candidate information.
10. Do not blindly follow reviewer suggestions if they would require unsupported information.
11. Improve wording, relevance, keyword coverage, structure, and emphasis where appropriate.
12. Preserve factual information from the original resume.
13. Only make changes that are supported by the candidate data and relevant to the target job.
14. Return the COMPLETE improved resume, not only the changed sections.

HEADER INFORMATION RULES:
- Preserve the candidate's name exactly.
- Include email only if provided.
- Include phone only if provided.
- Include location only if provided.
- Include GitHub URL only if provided.
- Include LinkedIn URL only if provided.
- Include portfolio URL only if provided.
- Never invent contact information.
- Never modify or fabricate URLs.

{format_instructions}

TARGET JOB ANALYSIS:
{job_analysis}

CANDIDATE ANALYSIS:
{candidate_analysis}

ORIGINAL CANDIDATE INFORMATION:
{candidate_profile}

CURRENT RESUME:
{existing_resume}

REVIEWER FEEDBACK:
{review}

Return ONLY the JSON object. No extra text, no markdown fences.
""",
            input_variables=["job_analysis", "candidate_analysis", "candidate_profile", "existing_resume", "review"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt_template | llm | parser
        result = chain.invoke({
            "job_analysis": job_analysis,
            "candidate_analysis": candidate_analysis,
            "candidate_profile": candidate_profile,
            "existing_resume": existing_resume,
            "review": review,
        })

    return result