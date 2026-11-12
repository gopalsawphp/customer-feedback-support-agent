
from typing import Literal, TypedDict, Optional

from pydantic import BaseModel, Field


class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(...,
        description="Overall customer feedback sentiment"
    )
    reason: str = Field(
        description="Short explanation for the classification"
    )


class FeedbackAnalysis(BaseModel):
    issue_type: Literal[
        "product_quality",
        "delivery",
        "billing",
        "technical_support",
        "customer_service",
        "refund",
        "other",
    ]
    tone: Literal[
        "angry",
        "frustrated",
        "disappointed",
        "concerned",
        "neutral",
    ]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(
        description="Concise summary of the customer's problem"
    )
    suggested_action: str = Field(
        description="Recommended next step; do not claim an action has happened"
    )


class EmailDraft(BaseModel):
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Complete professional email body")


class EmailDraftReview(TypedDict):
    subject: str
    body: str
    score: int


class FeedbackState(TypedDict):
    customer_name: str
    customer_email: str
    feedback: str
    sentiment: str
    sentiment_reason: Optional[str]
    analysis: Optional[dict]
    email_subject: Optional[str]
    email_body: Optional[str]
    email_status: Optional[str]
    approval_status: Optional[Literal["approved", "rejected"]]
    email_clarification: Optional[str]
    email_review_attempts: int
    email_draft_history: list[EmailDraftReview]
    email_selected_score: Optional[int]
    email_auto_send_best: bool

