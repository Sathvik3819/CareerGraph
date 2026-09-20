from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.graph.workflow import build_resume_graph
from app.models.resume import ResumeRecord
from app.models.user import User
from app.pdf.generator import generate_resume_pdf
from app.schemas.request import (
    PDFGenerationRequest,
    ResumeGenerationRequest,
)
from app.schemas.response import (
    ResumeDetailResponse,
    ResumeGenerationResponse,
    ResumeHistoryResponse,
)
from app.utils.candidate_formatter import format_candidate_profile


def serialize_resume_value(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    if isinstance(value, dict):
        return {
            key: serialize_resume_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            serialize_resume_value(item)
            for item in value
        ]

    return value


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


@router.post(
    "/generate",
    response_model=ResumeGenerationResponse
)
def generate_resume(
    request: ResumeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        candidate_profile = format_candidate_profile(request)

        graph = build_resume_graph()

        initial_state = {
            "candidate_profile": candidate_profile,
            "job_description": f"""
Target Role:
{request.job_role}

Job Description:
{request.job_description}
""",
            "iteration": 0,
            "template": request.template
        }

        final_state = graph.invoke(initial_state)

        resume_record = ResumeRecord(
            user_id=current_user.id,
            candidate_name=request.personal.name,
            job_role=request.job_role,
            job_description=request.job_description,
            template=request.template,
            iterations=final_state.get("iteration", 0),
            candidate_data=request.model_dump(),
            resume_data=serialize_resume_value(final_state.get("resume", {})),
            review_data=serialize_resume_value(final_state.get("review", {})),
            ats_data=serialize_resume_value(final_state.get("ats_analysis", {})),
        )

        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)

        return ResumeGenerationResponse(
            resume_id=str(resume_record.id),
            status=final_state.get("status", "completed"),
            iterations=final_state.get("iteration", 0),
            resume=final_state["resume"],
            review=final_state["review"],
            ats_analysis=final_state["ats_analysis"],
            pdf_path=final_state.get("pdf_path")
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/history",
    response_model=ResumeHistoryResponse
)
def get_resume_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(ResumeRecord)
        .filter(ResumeRecord.user_id == current_user.id)
        .order_by(ResumeRecord.created_at.desc())
        .all()
    )

    resumes = []

    for record in records:
        resumes.append(
            {
                "id": str(record.id),
                "candidate_name": record.candidate_name,
                "job_role": record.job_role,
                "template": record.template,
                "iterations": record.iterations,
                "ats_score": record.ats_data.get("overall_score", 0),
                "review_score": record.review_data.get("score", 0),
                "decision": record.review_data.get("decision", "UNKNOWN"),
                "created_at": record.created_at,
            }
        )

    return {
        "resumes": resumes
    }


@router.get(
    "/{resume_id}",
    response_model=ResumeDetailResponse
)
def get_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = (
        db.query(ResumeRecord)
        .filter(
            ResumeRecord.id == resume_id,
            ResumeRecord.user_id == current_user.id,
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return {
        "id": str(record.id),
        "candidate_name": record.candidate_name,
        "job_role": record.job_role,
        "job_description": record.job_description,
        "template": record.template,
        "iterations": record.iterations,
        "candidate_data": record.candidate_data,
        "resume": record.resume_data,
        "review": record.review_data,
        "ats_analysis": record.ats_data,
        "created_at": record.created_at,
    }


@router.post("/pdf")
def generate_pdf(request: PDFGenerationRequest):
    output_path = f"careergraph_{request.template}.pdf"

    generate_resume_pdf(
        resume=request.resume,
        output_path=output_path,
        template=request.template
    )

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=f"careergraph_{request.template}_resume.pdf"
    )


@router.get("/download")
def download_resume(template: str = "modern"):
    pdf_path = Path(f"generated_resume_{template}.pdf")

    if not pdf_path.exists():
        fallback_path = Path("generated_resume.pdf")
        if not fallback_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Resume PDF not found. Generate a resume first."
            )
        pdf_path = fallback_path

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"careergraph_resume_{template}.pdf"
    )