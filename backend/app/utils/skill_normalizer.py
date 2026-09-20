import re

SKILL_ALIASES = {
    # Programming languages
    "python3": "python",
    "py": "python",

    "javascript": "javascript",
    "js": "javascript",

    "typescript": "typescript",
    "ts": "typescript",

    "c++": "cpp",
    "cpp": "cpp",

    # Frontend
    "react.js": "react",
    "reactjs": "react",
    "react js": "react",

    "next.js": "nextjs",
    "nextjs": "nextjs",

    "vue.js": "vue",
    "vuejs": "vue",

    # Backend
    "node": "nodejs",
    "node.js": "nodejs",
    "nodejs": "nodejs",

    "express.js": "express",
    "expressjs": "express",

    # Databases
    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mongo": "mongodb",
    "mongo db": "mongodb",
    "mongodb": "mongodb",

    # AI / GenAI
    "lang chain": "langchain",
    "langchain": "langchain",

    "lang graph": "langgraph",
    "langgraph": "langgraph",

    "llm": "llm",
    "large language model": "llm",

    "rag": "rag",
    "retrieval augmented generation": "rag",

    "vector db": "vector database",
    "vector dbs": "vector database",
    "vector database": "vector database",
    "vector databases": "vector database",

    # APIs / frameworks
    "fast api": "fastapi",
    "fastapi": "fastapi",

    "rest api": "rest api",
    "rest apis": "rest api",

    # Cloud
    "amazon web services": "aws",
    "aws": "aws",

    "google cloud platform": "gcp",
    "gcp": "gcp",

    "microsoft azure": "azure",
    "azure": "azure",
}


def normalize_skill(skill: str) -> str:
    """
    Convert a skill or technology into a canonical representation.
    """

    if skill is None:
        return ""

    skill = str(skill).lower().strip()
    skill = re.sub(r"\s+", " ", skill)

    return SKILL_ALIASES.get(skill, skill)


def normalize_skills(skills: list[str]) -> set[str]:
    """
    Normalize a list of skills and remove duplicates.
    """

    return {
        normalize_skill(skill)
        for skill in skills
        if str(skill).strip()
    }
