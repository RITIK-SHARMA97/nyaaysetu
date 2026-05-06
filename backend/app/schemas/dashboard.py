from pydantic import BaseModel
from typing import Optional

class DeptLeaderboardEntry(BaseModel):
    department: str
    compliance_score: float
    total_actions: int
    complied_actions: int
    overdue_actions: int
    critical_actions: int
    trend: str

    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_actions: int
    overdue_actions: int
    critical_actions: int
    complied_today: int
    leaderboard: list[DeptLeaderboardEntry]

class BriefingAction(BaseModel):
    id: str
    directive_text: str
    responsible_designation: str
    due_date: Optional[str]
    days_left: Optional[int]
    contempt_risk: str
    status: str
    case_number: Optional[str]

class BriefingResponse(BaseModel):
    officer_name: str
    department: str
    inherited_count: int
    actions: list[BriefingAction]
