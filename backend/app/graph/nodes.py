from app.agents.ats_analyzer import analyze_ats
from app.agents.profile_analyer import analyze_candidate_profile
from app.agents.jd_analyzer import analyze_job_description
from app.agents.resume_creator import create_resume
from app.agents.reviewer import review_resume

from app.graph.state import ResumeState


def analyze_profile_node(state: ResumeState):
    result = analyze_candidate_profile(
        state["candidate_profile"]
    )

    return {
        "candidate_analysis": result
    }


def analyze_job_node(state: ResumeState):
    result = analyze_job_description(
        state["job_description"]
    )

    return {
        "job_analysis": result
    }


def create_resume_node(state: ResumeState):

    result = create_resume(
        candidate_profile=state["candidate_profile"],
        candidate_analysis=state["candidate_analysis"],
        job_analysis=state["job_analysis"],
        existing_resume=state.get("resume"),
        review=state.get("review")
    )

    current_iteration = state.get("iteration", 0)

    return {
        "resume": result,
        "iteration": current_iteration + 1
    }


def review_resume_node(state: ResumeState):

    result = review_resume(
        candidate_profile=state["candidate_profile"],
        candidate_analysis=state["candidate_analysis"],
        job_description=state["job_description"],
        job_analysis=state["job_analysis"],
        resume=state["resume"]
    )

    return {
        "review": result
    }


def analyze_ats_node(state: ResumeState):

    result = analyze_ats(
        resume=state["resume"],
        job_analysis=state["job_analysis"],
    )

    return {
        "ats_analysis": result
    }
    

def route_after_review(state: ResumeState):

    review = state["review"]

    # Resume is good enough
    if review.decision == "APPROVED":
        return "approved"

    # Maximum number of resume generations reached
    if state.get("iteration", 0) >= 3:
        return "max_iterations"

    # Resume needs improvement
    return "revise"