from pathlib import Path
from functools import lru_cache
from langgraph.types import Command
from app.agents.agent import agent_manager
from app.schemas.schema import FeedbackState


@lru_cache(maxsize=1)
def _get_graph():
    return agent_manager()


def _thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


# ---------- RUN THE WORKFLOW ----------

def customer_feedback_Analysis(
    feedback: str,
    customer_name: str,
    customer_email: str,
    thread_id: str,
) -> FeedbackState:
    graph = _get_graph()
    graph_path = Path("customer_feedback_graph.png")
    if not graph_path.exists():
        graph_png = graph.get_graph().draw_mermaid_png()
        graph_path.write_bytes(graph_png)
    else:
        print("Graph already exists. Skipping generation.")

    initial_state: FeedbackState = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "feedback": feedback,
        "sentiment": None,
        "sentiment_reason": None,
        "analysis": None,
        "email_subject": None,
        "email_body": None,
        "email_status": "awaiting_approval",
        "approval_status": None,
        "email_clarification": None,
        "email_review_attempts": 0,
        "email_draft_history": [],
        "email_selected_score": None,
        "email_auto_send_best": False,
    }

    config = _thread_config(thread_id)
    graph.invoke(initial_state, config=config)
    return graph.get_state(config).values


def resume_customer_feedback_Analysis(
    thread_id: str,
    approval_status: str,
    score: int,
    clarification: str = "",
) -> FeedbackState:
    approval_status = approval_status.strip().lower()
    if approval_status not in {"approved", "rejected"}:
        raise ValueError("Enter 'approved' or 'rejected' as the approval status.")
    if type(score) is not int or not 1 <= score <= 10:
        raise ValueError("Enter a score from 1 to 10 for this email.")
    if approval_status == "rejected" and not clarification.strip():
        raise ValueError("Please explain what should change in the email.")

    graph = _get_graph()
    config = _thread_config(thread_id)
    graph.invoke(
        Command(
            resume={
                "approval_status": approval_status,
                "score": score,
                "clarification": clarification,
            }
        ),
        config=config,
    )
    return graph.get_state(config).values