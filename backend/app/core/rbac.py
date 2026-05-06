PERMISSIONS = {
    "reviewer": ["upload_judgment", "verify_fields", "view_dashboard"],
    "officer": ["view_dashboard", "update_action_status", "view_briefing", "generate_affidavit"],
    "head": ["view_dashboard", "update_action_status", "view_briefing", "generate_affidavit", "view_all_dept"],
    "secretary": ["view_dashboard", "view_all_dept", "view_leaderboard", "override_status"],
    "admin": ["upload_judgment", "verify_fields", "view_dashboard", "update_action_status",
              "view_briefing", "generate_affidavit", "view_all_dept", "view_leaderboard", "override_status"],
}

def has_permission(role: str, permission: str) -> bool:
    return permission in PERMISSIONS.get(role, [])

def check_permission(user: dict, permission: str):
    from fastapi import HTTPException
    if not has_permission(user.get("role", ""), permission):
        raise HTTPException(status_code=403, detail=f"Permission denied: {permission}")
