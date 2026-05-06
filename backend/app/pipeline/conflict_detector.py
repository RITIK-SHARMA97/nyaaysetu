import re

def detect_conflicts(new_actions: list[dict], existing_actions: list) -> list[dict]:
    """Check new actions against existing DB actions for same dept/subject conflicts."""
    conflicts = []
    for new in new_actions:
        new_dept = new.get("responsible_department", "").lower()
        new_text = new.get("directive_text", "").lower()
        new_words = set(re.findall(r'\b\w{4,}\b', new_text))
        
        for existing in existing_actions:
            ex_dept = (existing.responsible_department or "").lower()
            ex_text = (existing.directive_text or "").lower()
            ex_words = set(re.findall(r'\b\w{4,}\b', ex_text))
            
            if new_dept == ex_dept and new_dept:
                # Check word overlap
                overlap = new_words & ex_words
                similarity = len(overlap) / max(len(new_words), 1)
                if similarity > 0.4:
                    conflicts.append({
                        "new_directive": new.get("directive_text"),
                        "existing_directive": existing.directive_text,
                        "existing_action_id": existing.id,
                        "department": new.get("responsible_department"),
                        "similarity_score": round(similarity, 2),
                        "conflict_type": "potentially_contradictory"
                    })
    return conflicts
