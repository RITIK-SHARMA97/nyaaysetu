from datetime import datetime, timedelta
from typing import Optional

APPEAL_WINDOWS = [
    {"appeal_type": "writ_appeal", "window_days": 30, "legal_basis": "Order 41 Rule 1, CPC / Section 5 Limitation Act"},
    {"appeal_type": "slp", "window_days": 90, "legal_basis": "Article 136, Constitution of India"},
    {"appeal_type": "lp_appeal", "window_days": 30, "legal_basis": "Letters Patent Clause 15"},
]

def calculate_appeal_windows(order_date: Optional[str]) -> list[dict]:
    if not order_date:
        base = datetime.now()
    else:
        try:
            base = datetime.strptime(order_date, '%Y-%m-%d')
        except:
            base = datetime.now()
    
    windows = []
    for w in APPEAL_WINDOWS:
        deadline = base + timedelta(days=w["window_days"])
        days_remaining = (deadline - datetime.now()).days
        windows.append({
            **w,
            "deadline_date": deadline.strftime('%Y-%m-%d'),
            "days_remaining": max(0, days_remaining),
        })
    return windows
