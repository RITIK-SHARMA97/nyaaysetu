from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.action import ActionItem
from app.core.security import get_current_user

router = APIRouter(prefix="/officers", tags=["Officers"])

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user

@router.get("/briefing")
def get_briefing(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    dept = user.get("dept", "")
    q = db.query(ActionItem)
    if dept and user.get("role") in ["officer", "head"]:
        q = q.filter(ActionItem.responsible_department == dept)
    actions = q.filter(
        ActionItem.status.in_(["new", "approved", "assigned", "in_progress", "escalated", "overdue"])
    ).order_by(ActionItem.days_left.asc().nullslast()).limit(50).all()

    return {
        "officer_name": user.get("name", "Officer"),
        "department": dept,
        "role": user.get("role"),
        "inherited_count": len(actions),
        "actions": [{
            "id": a.id,
            "directive_text": a.directive_text,
            "responsible_designation": a.responsible_designation,
            "due_date": a.due_date,
            "days_left": a.days_left,
            "contempt_risk": a.contempt_risk,
            "status": a.status,
            "judgment_id": a.judgment_id,
        } for a in actions]
    }
