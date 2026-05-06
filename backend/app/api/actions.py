import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.action import ActionItem
from app.models.audit import AuditLog
from app.schemas.action import ActionPatch, ActionStatusPatch
from app.core.security import get_current_user
from app.pipeline.affidavit import generate_affidavit

router = APIRouter(prefix="/actions", tags=["Actions"])

@router.get("/")
def list_actions(
    status: str = None,
    risk: str = None,
    department: str = None,
    page: int = 1,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    q = db.query(ActionItem)
    if status:
        q = q.filter(ActionItem.status == status)
    if risk:
        q = q.filter(ActionItem.contempt_risk == risk)
    if department:
        q = q.filter(ActionItem.responsible_department == department)
    total = q.count()
    items = q.order_by(ActionItem.days_left.asc().nullslast()).offset((page-1)*20).limit(20).all()
    return {"total": total, "page": page, "items": [_serialize(a) for a in items]}

@router.get("/{action_id}")
def get_action(action_id: str, db: Session = Depends(get_db)):
    a = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not a:
        raise HTTPException(404, "Action not found")
    result = _serialize(a)
    result["audit_logs"] = [_serialize_audit(log) for log in a.audit_logs]
    return result

@router.patch("/{action_id}")
def verify_action(
    action_id: str,
    patch: ActionPatch,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    a = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not a:
        raise HTTPException(404, "Action not found")

    old_value = a.directive_text
    if patch.decision == "approve":
        a.status = "approved"
    elif patch.decision == "edit" and patch.edited_value:
        a.directive_text = patch.edited_value
        a.status = "approved"
    elif patch.decision == "reject":
        a.status = "new"

    log = AuditLog(
        id=str(uuid.uuid4()),
        action_item_id=action_id,
        officer_email=user.get("email", "unknown"),
        officer_name=user.get("name", "Unknown"),
        event_type=patch.decision,
        old_value=old_value,
        new_value=a.directive_text,
        notes=patch.notes
    )
    db.add(log)
    db.commit()
    return _serialize(a)

@router.patch("/{action_id}/status")
def update_status(
    action_id: str,
    patch: ActionStatusPatch,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    a = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not a:
        raise HTTPException(404, "Action not found")

    valid_transitions = {
        "new": ["under_review", "approved"],
        "under_review": ["approved", "new"],
        "approved": ["assigned", "in_progress"],
        "assigned": ["in_progress"],
        "in_progress": ["complied", "escalated"],
        "complied": ["verified"],
        "verified": ["closed"],
        "escalated": ["in_progress", "complied"],
        "overdue": ["in_progress", "complied"],
    }
    allowed = valid_transitions.get(a.status, [])
    if patch.status not in allowed and user.get("role") not in ["admin", "secretary"]:
        raise HTTPException(400, f"Cannot transition from '{a.status}' to '{patch.status}'")

    old_status = a.status
    a.status = patch.status

    log = AuditLog(
        id=str(uuid.uuid4()),
        action_item_id=action_id,
        officer_email=user.get("email", "unknown"),
        officer_name=user.get("name", "Unknown"),
        event_type="status_changed",
        old_value=old_status,
        new_value=patch.status,
        notes=patch.notes
    )
    db.add(log)
    db.commit()
    return _serialize(a)

@router.get("/{action_id}/affidavit")
def get_affidavit(action_id: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    a = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    if not a:
        raise HTTPException(404, "Action not found")
    if a.status not in ["complied", "verified"]:
        raise HTTPException(400, "Affidavit only available for complied actions")
    j = a.judgment
    action_dict = {
        "directive_text": a.directive_text,
        "responsible_designation": a.responsible_designation,
        "responsible_department": a.responsible_department,
        "judgment_case_number": j.case_number if j else "",
        "order_date": j.order_date if j else "",
    }
    text = generate_affidavit(action_dict, user)
    return {"affidavit_text": text, "action_id": action_id}

def _serialize(a: ActionItem) -> dict:
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
        "created_at": str(a.created_at) if a.created_at else None,
    }

def _serialize_audit(log: AuditLog) -> dict:
    return {
        "id": log.id,
        "officer_email": log.officer_email,
        "officer_name": log.officer_name,
        "event_type": log.event_type,
        "old_value": log.old_value,
        "new_value": log.new_value,
        "notes": log.notes,
        "created_at": str(log.created_at) if log.created_at else None,
    }
