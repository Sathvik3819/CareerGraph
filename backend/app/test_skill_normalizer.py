from app.utils.skill_normalizer import (
    normalize_skill,
    normalize_skills,
)


tests = [
    "React.js",
    "ReactJS",
    "React",
    "Postgres",
    "PostgreSQL",
    "Node.js",
    "Node",
    "MongoDB",
    "LangChain",
    "Vector DB",
]

for skill in tests:
    print(f"{skill:20} -> {normalize_skill(skill)}")

print("\nUnique normalized skills:")
for skill in sorted(normalize_skills(tests)):
    print("-", skill)
