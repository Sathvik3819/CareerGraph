import shutil
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)


def escape_latex(value):
    if value is None:
        return ""

    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    for original, escaped in replacements.items():
        text = text.replace(original, escaped)

    return text


def _format_contact_line(resume):
    items = []
    if getattr(resume.header, "email", None):
        items.append(resume.header.email)
    if getattr(resume.header, "phone", None):
        items.append(resume.header.phone)
    if getattr(resume.header, "location", None):
        items.append(resume.header.location)
    if getattr(resume.header, "linkedin_url", None):
        items.append(f"\\href{{{resume.header.linkedin_url}}}{{LinkedIn}}")
    if getattr(resume.header, "github_url", None):
        items.append(f"\\href{{{resume.header.github_url}}}{{GitHub}}")
    if getattr(resume.header, "portfolio_url", None):
        items.append(f"\\href{{{resume.header.portfolio_url}}}{{Portfolio}}")

    return r" \textbar{} ".join(escape_latex(item) for item in items if item)


def _format_bullets(items):
    if not items:
        return ""

    rendered = []
    for item in items:
        safe_item = escape_latex(item).replace("\n", " ")
        rendered.append(f"\\item {safe_item}")
    return "\\begin{itemize}[leftmargin=1.2em, itemsep=0.18em]\n" + "\n".join(rendered) + "\n\\end{itemize}"


def _group_skills(skills):
    categories = {
        "Programming Languages": ["python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin"],
        "Frontend": ["react", "nextjs", "vue", "html", "css", "javascript", "typescript", "tailwind", "redux", "sass"],
        "Backend & APIs": ["fastapi", "django", "flask", "nodejs", "express", "rest api", "graphql", "spring boot", "asp.net"],
        "Databases": ["postgresql", "mysql", "mongodb", "redis", "sqlite", "elasticsearch", "firebase"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "terraform", "linux", "bash"],
        "Tools": ["git", "github", "gitlab", "jira", "postman", "figma", "docker", "vscode"],
    }

    normalized = {category: [] for category in categories}
    for skill in skills:
        safe_skill = str(skill).strip()
        if not safe_skill:
            continue
        matched = False
        for category, keywords in categories.items():
            lower_skill = safe_skill.lower()
            if any(keyword in lower_skill for keyword in keywords):
                normalized.setdefault(category, []).append(safe_skill)
                matched = True
                break
        if not matched:
            normalized.setdefault("Other", []).append(safe_skill)

    ordered = []
    for category in [
        "Programming Languages",
        "Frontend",
        "Backend & APIs",
        "Databases",
        "Cloud & DevOps",
        "Tools",
        "Other",
    ]:
        items = normalized.get(category, [])
        if items:
            ordered.append((category, sorted(set(items), key=str.lower)))

    return ordered


def generate_latex_resume(resume, output_path: str, template: str = "modern") -> str:
    header = resume.header
    name = escape_latex(header.name)
    contact_line = _format_contact_line(resume)
    summary = escape_latex(resume.summary or "")

    education_section = ""
    for item in resume.education:
        degree = escape_latex(item.degree or "")
        institution = escape_latex(item.institution or "")
        duration = escape_latex(item.duration or "")
        grade = escape_latex(item.grade or "")
        if degree and grade:
            degree_text = f"{degree} ({grade})"
        else:
            degree_text = degree
        education_section += f"""\\textbf{{{institution}}} \\hfill {duration}\\\\
{degree_text}\\\\
"""

    skills_section = ""
    if resume.skills:
        skill_groups = _group_skills(resume.skills)
        rendered_groups = []
        for category, items in skill_groups:
            rendered_groups.append(f"\\textbf{{{escape_latex(category)}:}} {', '.join(escape_latex(item) for item in items)}")
        skills_section = "\\par\n".join(rendered_groups)

    projects_section = ""
    for project in resume.projects:
        title = escape_latex(project.name)
        links = []
        if getattr(project, "github_url", None):
            links.append(f"\\href{{{project.github_url}}}{{GitHub}}")
        if getattr(project, "live_url", None):
            links.append(f"\\href{{{project.live_url}}}{{Live}}")
        link_text = " | ".join(links)
        tech_text = ""
        if project.technologies:
            tech_text = "\\textit{" + " , ".join(escape_latex(tech) for tech in project.technologies) + "}\\\\\n"
        description = escape_latex(project.description or "")
        projects_section += f"""\\textbf{{{title}}}\\hfill {link_text}\\\\
{tech_text}
{description}\\\\
"""

    experience_section = ""
    for exp in resume.experience:
        role = escape_latex(exp.role)
        company = escape_latex(exp.company)
        duration = escape_latex(exp.duration)
        experience_section += f"""\\textbf{{{role}}} \\hfill {duration}\\\\
{company}\\\\
{_format_bullets(exp.description or [])}
"""

    certifications_section = ""
    if resume.certifications:
        certifications_section = _format_bullets(resume.certifications)

    template_text = rf"""\documentclass[10pt,a4paper]{{article}}
\usepackage[margin=0.7in]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\setmainfont{{Arial}}
\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\tabcolsep}}{{0pt}}
\renewcommand{{\arraystretch}}{{1.1}}
\begin{{document}}
\begin{{center}}
{{\bfseries\fontsize{{22}}{{26}}\selectfont {name}}}\par
{{\small {contact_line}}}
\end{{center}}
\vspace{{0.2cm}}

\noindent\textbf{{Summary}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{summary}
\vspace{{0.2cm}}

\noindent\textbf{{Education}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{education_section}
\vspace{{0.2cm}}

\noindent\textbf{{Skills}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{skills_section}
\vspace{{0.2cm}}

\noindent\textbf{{Projects}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{projects_section}
\vspace{{0.2cm}}

\noindent\textbf{{Experience}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{experience_section}
\vspace{{0.2cm}}

\noindent\textbf{{Achievements}}\par
\rule{{\linewidth}}{{0.5pt}}\par
{certifications_section}
\end{{document}}
"""

    tex_path = Path(output_path).with_suffix(".tex")
    tex_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path.write_text(template_text, encoding="utf-8")
    return template_text


def _resolve_xelatex_binary():
    candidate_names = [
        "xelatex",
        "xelatex.exe",
        "miktex-xelatex",
        "miktex-xelatex.exe",
    ]

    for name in candidate_names:
        resolved = shutil.which(name)
        if resolved:
            return resolved

    windows_paths = [
        Path(r"C:\Program Files\MiKTeX\miktex\bin\x64"),
        Path(r"C:\Program Files\MiKTeX\miktex\bin"),
        Path(r"C:\Users\dell\AppData\Local\Programs\MiKTeX\miktex\bin\x64"),
        Path(r"C:\Users\dell\AppData\Local\Programs\MiKTeX\miktex\bin"),
    ]

    for base in windows_paths:
        for name in candidate_names:
            binary = base / name
            if binary.exists():
                return str(binary)

    return None


def validate_latex(latex_text: str):
    required_markers = [
        "\\documentclass",
        "\\begin{document}",
        "\\end{document}",
    ]

    for marker in required_markers:
        if marker not in latex_text:
            raise ValueError(f"LaTeX template is invalid: missing {marker}")

    return True


def compile_latex_to_pdf(output_path: str):
    tex_path = Path(output_path).with_suffix(".tex")
    if not tex_path.exists():
        raise FileNotFoundError(f"LaTeX file not found: {tex_path}")

    xelatex = _resolve_xelatex_binary()
    if not xelatex:
        raise RuntimeError("XeLaTeX is not installed on this machine.")

    result = subprocess.run(
        [xelatex, "-interaction=nonstopmode", "-halt-on-error", str(tex_path)],
        cwd=str(tex_path.parent),
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        error_output = (result.stdout or "") + (result.stderr or "")
        raise RuntimeError(f"XeLaTeX compilation failed for {tex_path}: {error_output.strip()}")

    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"XeLaTeX compilation failed for {tex_path}")

    return str(pdf_path)


def _generate_reportlab_fallback(resume, output_path: str, template: str = "modern"):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    name_font = "Times-Roman"
    bold_font = "Times-Bold"
    body_font = "Times-Roman"

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Title"],
        fontName=name_font,
        fontSize=20,
        leading=24,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["BodyText"],
        fontName=body_font,
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=colors.black,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName=bold_font,
        fontSize=12,
        leading=14,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=1,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=body_font,
        fontSize=10,
        leading=13,
        spaceAfter=2,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
    )

    body_left_style = ParagraphStyle(
        "BodyLeft",
        parent=body_style,
        alignment=TA_LEFT,
    )

    body_right_style = ParagraphStyle(
        "BodyRight",
        parent=body_style,
        alignment=TA_RIGHT,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=24,
        firstLineIndent=-12,
        spaceBefore=2,
        spaceAfter=2,
    )

    story = []
    story.append(Paragraph(resume.header.name, name_style))

    contact_items = []
    if resume.header.email:
        contact_items.append(resume.header.email)
    if resume.header.linkedin_url:
        contact_items.append(f'<a href="{resume.header.linkedin_url}" color="black">LinkedIn</a>')
    if resume.header.github_url:
        contact_items.append(f'<a href="{resume.header.github_url}" color="black">GitHub</a>')
    if resume.header.portfolio_url:
        contact_items.append(f'<a href="{resume.header.portfolio_url}" color="black">Portfolio</a>')
    if resume.header.phone:
        contact_items.append(resume.header.phone)
    if resume.header.location:
        contact_items.append(resume.header.location)

    if contact_items:
        story.append(Paragraph(" — ".join(contact_items), contact_style))

    if resume.summary:
        story.append(Paragraph("Summary", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        story.append(Paragraph(resume.summary, body_style))
        story.append(Spacer(1, 4))

    if resume.education:
        story.append(Paragraph("Education", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        for ed in resume.education:
            row = Table([[Paragraph(f"<b>{ed.institution}</b>", body_left_style), Paragraph(ed.duration, body_right_style)]], colWidths=["75%", "25%"])
            row.setStyle(TableStyle([('PADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 1), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
            story.append(row)
            if ed.degree:
                degree_text = ed.degree
                if ed.grade:
                    degree_text += f" (Grade: {ed.grade})"
                story.append(Paragraph(degree_text, body_left_style))

    if resume.skills:
        story.append(Paragraph("Technical Skills", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        for skill in resume.skills:
            story.append(Paragraph(f"• {skill}", bullet_style))

    if resume.projects:
        story.append(Paragraph("Projects", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        for proj in resume.projects:
            link_text = " / ".join(filter(None, [f'<a href="{proj.github_url}" color="black">GitHub</a>' if getattr(proj, "github_url", None) else None, f'<a href="{proj.live_url}" color="black">Live</a>' if getattr(proj, "live_url", None) else None]))
            row = Table([[Paragraph(f"<b>{proj.name}</b>", body_left_style), Paragraph(link_text, body_right_style)]], colWidths=["85%", "15%"])
            row.setStyle(TableStyle([('PADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 1), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
            story.append(row)
            if proj.technologies:
                story.append(Paragraph(f"<i>{', '.join(proj.technologies)}</i>", body_left_style))
            for line in proj.description.split("\n"):
                line = line.strip()
                if line:
                    story.append(Paragraph(f"• {line}", bullet_style))

    if resume.experience:
        story.append(Paragraph("Experience", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        for exp in resume.experience:
            row = Table([[Paragraph(f"<b>{exp.role}</b>", body_left_style), Paragraph(exp.duration, body_right_style)]], colWidths=["75%", "25%"])
            row.setStyle(TableStyle([('PADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 1), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
            story.append(row)
            story.append(Paragraph(f"<i>{exp.company}</i>", body_left_style))
            for bullet in exp.description:
                story.append(Paragraph(f"• {bullet}", bullet_style))

    if resume.certifications:
        story.append(Paragraph("Achievements", section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=4))
        for cert in resume.certifications:
            story.append(Paragraph(f"• {cert}", bullet_style))

    document.build(story)
    return output_path


def generate_resume_pdf(resume, output_path: str, template: str = "modern"):
    """Generate a resume PDF using a fixed LaTeX template when XeLaTeX is available.
    Falls back to the ReportLab generator only when the compiler is truly missing.
    """

    output_path = str(output_path)
    tex_path = Path(output_path).with_suffix(".tex")
    latex = generate_latex_resume(resume, str(tex_path), template=template)
    validate_latex(latex)

    try:
        return compile_latex_to_pdf(str(tex_path))
    except RuntimeError as exc:
        message = str(exc)
        if "not installed" in message.lower():
            fallback_output = str(Path(output_path).with_suffix(".pdf"))
            if not Path(fallback_output).exists():
                return _generate_reportlab_fallback(resume, fallback_output, template=template)
            return fallback_output
        raise
