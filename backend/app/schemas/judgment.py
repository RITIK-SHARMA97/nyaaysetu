from pydantic import BaseModel
from typing import Optional

class JudgmentUploadResponse(BaseModel):
    judgment_id: str
    status: str
    message: str

class JudgmentStatus(BaseModel):
    judgment_id: str
    status: str
    progress: int
    message: Optional[str] = None

class ConfidenceScores(BaseModel):
    overall: float
    directive_detection: float
    department_routing: float
    deadline_extraction: float

class ActionItemOut(BaseModel):
    id: str
    directive_text: str
    source_page: int
    source_bbox: Optional[str] = None
    source_sentence: Optional[str] = None
    action_type: str
    responsible_designation: str
    responsible_department: Optional[str] = None
    due_date: Optional[str] = None
    due_date_basis: str
    days_left: Optional[int] = None
    contempt_risk: str
    confidence_overall: float
    confidence_directive: float
    confidence_department: float
    confidence_deadline: float
    status: str
    chain_next: Optional[str] = None

    class Config:
        from_attributes = True

class AppealWindowOut(BaseModel):
    appeal_type: str
    window_days: int
    deadline_date: Optional[str]
    days_remaining: Optional[int]
    legal_basis: str

    class Config:
        from_attributes = True

class JudgmentDetail(BaseModel):
    id: str
    case_number: Optional[str]
    order_date: Optional[str]
    pdf_filename: Optional[str]
    pdf_url: Optional[str] = None
    processing_status: str
    total_pages: int
    has_kannada: str
    action_items: list[ActionItemOut] = []
    appeal_windows: list[AppealWindowOut] = []

    class Config:
        from_attributes = True
