from datetime import datetime, timedelta
from typing import Optional
from app.pipeline.classifier import resolve_implicit_deadline, calculate_contempt_risk, calculate_days_left

def enrich_actions(raw_actions: list[dict], order_date: Optional[str] = None) -> list[dict]:
    """Add due_date, days_left, contempt_risk to each raw action."""
    enriched = []
    for action in raw_actions:
        due_date_text = action.get("due_date_text")
        days, basis, due_date = resolve_implicit_deadline(
            due_date_text or action.get("directive_text", ""),
            order_date
        )
        days_left = calculate_days_left(due_date)
        contempt_risk = calculate_contempt_risk(days_left)
        
        enriched.append({
            **action,
            "due_date": due_date,
            "due_date_basis": basis,
            "days_left": days_left,
            "contempt_risk": contempt_risk,
        })
    return enriched
