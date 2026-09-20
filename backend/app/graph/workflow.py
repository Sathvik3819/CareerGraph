from langgraph.graph import StateGraph, START, END

from app.graph.state import ResumeState
from app.pdf.node import generate_pdf_node
from app.graph.nodes import (
    analyze_ats_node,
    analyze_profile_node,
    analyze_job_node,
    create_resume_node,
    review_resume_node,
    route_after_review
)

from langchain_core.runnables import RunnableConfig

def build_resume_graph():

    graph = StateGraph(ResumeState)

    # -------------------------
    # Add nodes
    # -------------------------

    graph.add_node(
        "analyze_profile",
        analyze_profile_node
    )

    graph.add_node(
        "analyze_job",
        analyze_job_node
    )

    graph.add_node(
        "create_resume",
        create_resume_node
    )

    graph.add_node(
        "review_resume",
        review_resume_node
    )

    graph.add_node(
        "analyze_ats",
        analyze_ats_node
    )

    graph.add_node(
        "generate_pdf",
        generate_pdf_node
    )

    # -------------------------
    # Normal flow
    # -------------------------

    graph.add_edge(
        START,
        "analyze_profile"
    )

    graph.add_edge(
        "analyze_profile",
        "analyze_job"
    )

    graph.add_edge(
        "analyze_job",
        "create_resume"
    )

    graph.add_edge(
        "create_resume",
        "review_resume"
    )

    graph.add_edge(
        "review_resume",
        "analyze_ats"
    )

    # -------------------------
    # Conditional routing
    # -------------------------

    graph.add_conditional_edges(
        "analyze_ats",
        route_after_review,
        {
            "approved": "generate_pdf",
            "revise": "create_resume",
            "max_iterations": END
        }
    )

    graph.add_edge(
        "generate_pdf",
        END
    )
    
    return graph.compile()