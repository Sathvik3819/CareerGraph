from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.schemas.job import JobAnalysis

load_dotenv()

endpoint = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",
    task="text-generation",
    temperature=0.3,
    do_sample=False,
)
llm = ChatHuggingFace(llm=endpoint)

parser = PydanticOutputParser(pydantic_object=JobAnalysis)

prompt_template = PromptTemplate(
    template="""
You are a Job Description Analysis Agent.

Analyze the following job description.

Extract:
1. The job role
2. Required skills
3. Preferred skills
4. Main responsibilities
5. Important technical and domain keywords

Important rules:
- Only extract information supported by the job description.
- Do not invent skills or requirements.
- Keep skills concise.
- Keep responsibilities concise.

{format_instructions}

Job Description:

{job_description}

Return ONLY the JSON object. No extra text, no markdown fences.
""",
    input_variables=["job_description"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | llm | parser


def analyze_job_description(job_description: str) -> JobAnalysis:

    result = chain.invoke({"job_description": job_description})
    return result