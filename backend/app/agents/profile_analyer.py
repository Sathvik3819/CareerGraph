from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.schemas.candidate import CandidateAnalysis

load_dotenv()

endpoint = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="text-generation",
    temperature=0.3,
    do_sample=False,
)
llm = ChatHuggingFace(llm=endpoint)

parser = PydanticOutputParser(pydantic_object=CandidateAnalysis)

prompt_template = PromptTemplate(
    template="""
You are a Candidate Profile Analysis Agent.

Analyze the candidate information provided below.

Extract:
1. Technical skills
2. Soft skills
3. Strongest projects
4. Experience highlights
5. Certifications
6. Missing information that could be useful for creating a professional resume

Important rules:
- Only use information provided by the candidate.
- Never invent skills, experience, achievements, metrics, or certifications.
- Do not assume that the candidate has a skill simply because it is related to another skill.
- Keep the output concise.
- If a category has no information, return an empty list.

{format_instructions}

Candidate Information:

{candidate_profile}

Return ONLY the JSON object. No extra text, no markdown fences.
""",
    input_variables=["candidate_profile"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | llm | parser


def analyze_candidate_profile(
    candidate_profile: str
) -> CandidateAnalysis:

    result = chain.invoke({"candidate_profile": candidate_profile})
    return result