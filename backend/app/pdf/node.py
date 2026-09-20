from app.pdf.generator import generate_resume_pdf
from app.graph.state import ResumeState


def generate_pdf_node(state: ResumeState):

    template = state.get("template", "modern")
    output_path = f"generated_resume_{template}.pdf"

    generate_resume_pdf(
        resume=state["resume"],
        output_path=output_path,
        template=template
    )

    return {
        "pdf_path": output_path,
        "status": "completed"
    }