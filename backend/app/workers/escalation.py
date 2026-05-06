from datetime import datetime
from sqlalchemy.orm import Session
from app.models.action import ActionItem
from app.models.compliance import ComplianceHealth

def run_escalation_check(db: Session):
    """Check all pending actions and flag those near deadline."""
    now = datetime.now()
    actions = db.query(ActionItem).filter(
        ActionItem.status.in_(["new", "approved", "assigned", "in_progress"])
    ).all()

    for action in actions:
        if not action.due_date:
            continue
        try:
            due = datetime.strptime(action.due_date, '%Y-%m-%d')
            days_left = (due - now).days
            action.days_left = days_left

            if days_left < 0:
                action.status = "overdue"
                action.contempt_risk = "critical"
                action.is_escalated = True
            elif days_left <= 7:
                action.contempt_risk = "critical"
                action.is_escalated = True
            elif days_left <= 15:
                action.contempt_risk = "red"
            elif days_left <= 30:
                action.contempt_risk = "amber"
            else:
                action.contempt_risk = "green"
        except:
            pass

    db.commit()
    _refresh_leaderboard(db)

def _refresh_leaderboard(db: Session):
    """Recalculate compliance health scores for all departments."""
    depts = db.query(ActionItem.responsible_department).distinct().all()
    for (dept,) in depts:
        if not dept:
            continue
        actions = db.query(ActionItem).filter(ActionItem.responsible_department == dept).all()
        total = len(actions)
        complied = sum(1 for a in actions if a.status in ["complied", "verified"])
        overdue = sum(1 for a in actions if a.status == "overdue" or (a.days_left is not None and a.days_left < 0))
        critical = sum(1 for a in actions if a.contempt_risk == "critical")
        ch = db.query(ComplianceHealth).filter(ComplianceHealth.department == dept).first()
        if not ch:
            import uuid
            ch = ComplianceHealth(id=str(uuid.uuid4()), department=dept)
            db.add(ch)
            ch.compliance_score = round((complied / total * 100) if total > 0 else 100.0, 1)
            ch.trend = "stable"
        ch.total_actions = total
        ch.complied_actions = complied
        ch.overdue_actions = overdue
        ch.critical_actions = critical
    db.commit()
