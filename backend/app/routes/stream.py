import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.graph.workflow import build_resume_graph
from app.models.resume import ResumeRecord
from app.models.user import User
from app.schemas.request import ResumeGenerationRequest
from app.utils.candidate_formatter import format_candidate_profile

router = APIRouter(
    prefix="/api/resume",
    tags=["Resume Streaming"],
)


def serialize_value(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    if isinstance(value, dict):
        return {
            key: serialize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            serialize_value(item)
            for item in value
        ]

    return value


@router.post("/stream")
def stream_resume(
    request: ResumeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate_profile = format_candidate_profile(request)

    initial_state = {
        "candidate_profile": candidate_profile,
        "job_description": f"""
Target Role:
{request.job_role}

Job Description:
{request.job_description}
""",
        "iteration": 0,
        "template": request.template,
    }

    def event_stream():
        current_state = initial_state.copy()

        try:
            graph = build_resume_graph()

            for update in graph.stream(initial_state, stream_mode="updates"):
                for node_name, node_output in update.items():
                    if node_output is None:
                        continue

                    yield (
                        "data: "
                        + json.dumps({
                            "type": "node_started",
                            "node": node_name,
                        })
                        + "\n\n"
                    )

                    current_state.update(node_output)

                    yield (
                        "data: "
                        + json.dumps({
                            "type": "node_completed",
                            "node": node_name,
                        })
                        + "\n\n"
                    )

            final_result = serialize_value(current_state)

            resume_record = ResumeRecord(
                user_id=current_user.id,
                candidate_name=request.personal.name,
                job_role=request.job_role,
                job_description=request.job_description,
                template=request.template,
                iterations=final_result.get("iteration", 0),
                candidate_data=serialize_value(request),
                resume_data=serialize_value(final_result.get("resume", {})),
                review_data=serialize_value(final_result.get("review", {})),
                ats_data=serialize_value(final_result.get("ats_analysis", {})),
            )

            db.add(resume_record)
            db.commit()
            db.refresh(resume_record)

            yield (
                "data: "
                + json.dumps({
                    "type": "completed",
                    "result": final_result,
                })
                + "\n\n"
            )

        except Exception as error:
            yield (
                "data: "
                + json.dumps({
                    "type": "error",
                    "message": str(error),
                })
                + "\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.post("/generate-stream")
def generate_resume_stream(
    request: ResumeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stream_resume(request=request, db=db, current_user=current_user)
