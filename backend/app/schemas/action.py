from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ContemptRisk(str, Enum):
    green = "green"
    amber = "amber"
    red = "red"
    critical = "critical"

class ActionStatus(str, Enum):
    new = "new"
    under_review = "under_review"
    approved = "approved"
    assigned = "assigned"
    in_progress = "in_progress"
    complied = "complied"
    verified = "verified"
    escalated = "escalated"
    overdue = "overdue"

class ActionPatch(BaseModel):
    decision: str  # approve/edit/reject
    edited_value: Optional[str] = None
    notes: Optional[str] = None

class ActionStatusPatch(BaseModel):
    status: str
    notes: Optional[str] = None

class AuditLogOut(BaseModel):
    id: str
    officer_email: str
    officer_name: Optional[str]
    event_type: str
    old_value: Optional[str]
    new_value: Optional[str]
    notes: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
