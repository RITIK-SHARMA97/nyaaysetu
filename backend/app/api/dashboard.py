from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.action import ActionItem
from app.models.compliance import ComplianceHealth
from app.core.security import get_current_user
from app.workers.escalation import run_escalation_check

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    run_escalation_check(db)
    total = db.query(ActionItem).count()
    overdue = db.query(ActionItem).filter(ActionItem.status == "overdue").count()
    critical = db.query(ActionItem).filter(ActionItem.contempt_risk == "critical").count()
    complied = db.query(ActionItem).filter(ActionItem.status.in_(["complied", "verified"])).count()
    leaderboard = db.query(ComplianceHealth).order_by(ComplianceHealth.compliance_score.desc()).all()
    return {
        "total_actions": total,
        "overdue_actions": overdue,
        "critical_actions": critical,
        "complied_actions": complied,
        "leaderboard": [_serialize_ch(ch) for ch in leaderboard]
    }

@router.get("/actions")
def get_actions(
    page: int = 1,
    status: str = None,
    risk: str = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    q = db.query(ActionItem)
    dept = user.get("dept")
    if user.get("role") in ["officer", "head"] and dept:
        q = q.filter(ActionItem.responsible_department == dept)
    if status:
        q = q.filter(ActionItem.status == status)
    if risk:
        q = q.filter(ActionItem.contempt_risk == risk)
    total = q.count()
    items = q.order_by(ActionItem.days_left.asc().nullslast()).offset((page-1)*20).limit(20).all()
    return {
        "total": total,
        "page": page,
        "items": [_serialize_action(a) for a in items]
    }

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    run_escalation_check(db)
    leaderboard = db.query(ComplianceHealth).order_by(ComplianceHealth.compliance_score.desc()).all()
    return [_serialize_ch(ch) for ch in leaderboard]

def _serialize_ch(ch: ComplianceHealth) -> dict:
    return {
        "department": ch.department,
        "compliance_score": ch.compliance_score,
        "total_actions": ch.total_actions,
        "complied_actions": ch.complied_actions,
        "overdue_actions": ch.overdue_actions,
        "critical_actions": ch.critical_actions,
        "trend": ch.trend,
    }

def _serialize_action(a: ActionItem) -> dict:
    return {
        "id": a.id,
        "judgment_id": a.judgment_id,
        "directive_text": a.directive_text,
        "source_page": a.source_page,
        "source_bbox": a.source_bbox,
        "source_sentence": a.source_sentence,
        "action_type": a.action_type,
        "responsible_designation": a.responsible_designation,
        "responsible_department": a.responsible_department,
        "due_date": a.due_date,
        "due_date_basis": a.due_date_basis,
        "days_left": a.days_left,
        "contempt_risk": a.contempt_risk,
        "confidence_overall": a.confidence_overall,
        "confidence_directive": a.confidence_directive,
        "confidence_department": a.confidence_department,
        "confidence_deadline": a.confidence_deadline,
        "status": a.status,
        "is_escalated": a.is_escalated,
        "chain_next": a.chain_next,
    }
