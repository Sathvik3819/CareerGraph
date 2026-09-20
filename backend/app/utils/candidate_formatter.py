def format_candidate_profile(request) -> str:
    personal = request.personal

    sections = []

    sections.append(
        f"""
PERSONAL INFORMATION

Name: {personal.name}
Email: {personal.email or ""}
Phone: {personal.phone or ""}
Location: {personal.location or ""}
GitHub: {personal.github or ""}
LinkedIn: {personal.linkedin or ""}
Portfolio: {personal.portfolio or ""}
"""
    )

    if request.education:
        education_text = "\n".join(
            [
                (
                    f"- {item.degree} at {item.institution} ({item.duration})"
                    + (f", Grade: {item.grade}" if item.grade else "")
                )
                for item in request.education
            ]
        )

        sections.append(
            f"""
EDUCATION

{education_text}
"""
        )

    if request.skills:
        sections.append(
            f"""
SKILLS

{', '.join(request.skills)}
"""
        )

    if request.projects:
        project_text = []

        for project in request.projects:
            project_text.append(
                f"""
Project: {project.name}
Description: {project.description}
Technologies: {', '.join(project.technologies)}
GitHub: {project.github_url or ""}
Live URL: {project.live_url or ""}
"""
            )

        sections.append("PROJECTS\n" + "\n".join(project_text))

    if request.experience:
        experience_text = []

        for experience in request.experience:
            experience_text.append(
                f"""
Role: {experience.role}
Company: {experience.company}
Duration: {experience.duration}
Description: {experience.description}
"""
            )

        sections.append("EXPERIENCE\n" + "\n".join(experience_text))

    if request.certifications:
        sections.append(
            f"""
CERTIFICATIONS

{', '.join(request.certifications)}
"""
        )

    return "\n".join(sections)
