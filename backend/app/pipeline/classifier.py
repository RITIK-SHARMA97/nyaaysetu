import re
from datetime import datetime, timedelta
from typing import Optional

HIGH_CONFIDENCE_VERBS = [
    r'\bis\s+directed\s+to\b', r'\bare\s+directed\s+to\b',
    r'\bshall\b', r'\bis\s+hereby\s+ordered\b',
    r'\bis\s+required\s+to\b', r'\bmust\b',
    r'\bis\s+commanded\s+to\b', r'\bforthwith\b',
    r'\bstand\s+directed\b', r'\bhereby\s+directed\b',
]
MEDIUM_CONFIDENCE_VERBS = [
    r'\bis\s+requested\s+to\b', r'\bwould\s+be\s+appropriate\b',
    r'\bshould\b', r'\bought\s+to\b',
]
IMPLICIT_DEADLINE_MAP = {
    'forthwith': 7,
    'at the earliest': 14,
    'expeditiously': 30,
    'as soon as possible': 21,
    'without delay': 7,
    'immediately': 3,
    'at an early date': 30,
    'without further delay': 7,
    'without any further delay': 7,
}

DEPT_KEYWORDS = {
    'Revenue Department': ['revenue', 'land', 'survey', 'mutation', 'khata', 'patta'],
    'Education Department': ['school', 'education', 'teacher', 'student', 'college'],
    'Urban Development': ['bbmp', 'bda', 'urban', 'municipality', 'building', 'plan'],
    'Health Department': ['hospital', 'health', 'medical', 'doctor', 'patient'],
    'Police Department': ['police', 'fir', 'investigation', 'arrest', 'station'],
    'Public Works Department': ['road', 'construction', 'tender', 'contractor', 'pwdm'],
    'Forest Department': ['forest', 'tree', 'encroachment', 'wildlife'],
}

def classify_sentence(sentence: str) -> dict:
    s = sentence.lower()
    for pattern in HIGH_CONFIDENCE_VERBS:
        if re.search(pattern, s):
            return {"is_directive": True, "confidence": 0.92, "tier": "HIGH"}
    for pattern in MEDIUM_CONFIDENCE_VERBS:
        if re.search(pattern, s):
            return {"is_directive": True, "confidence": 0.65, "tier": "MEDIUM"}
    return {"is_directive": False, "confidence": 0.1, "tier": "NONE"}

def resolve_implicit_deadline(text: str, order_date: Optional[str] = None) -> tuple:
    """Returns (days: int|None, basis: str, due_date: str|None)"""
    t = text.lower()

    # Check explicit day mentions first: "within 30 days", "within 8 weeks"
    explicit_days = re.search(r'within\s+(\d+)\s+(days?|weeks?|months?)', t)
    if explicit_days:
        num = int(explicit_days.group(1))
        unit = explicit_days.group(2)
        if 'week' in unit:
            num *= 7
        elif 'month' in unit:
            num *= 30
        due = _add_days(order_date, num)
        return num, f"explicit_{num}d", due

    # Check explicit date: "on or before 31.03.2024"
    date_match = re.search(r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})', text)
    if date_match:
        try:
            d = datetime.strptime(date_match.group(), '%d.%m.%Y')
            return None, "explicit_date", d.strftime('%Y-%m-%d')
        except:
            pass

    # Check implicit keywords
    for phrase, days in IMPLICIT_DEADLINE_MAP.items():
        if phrase in t:
            due = _add_days(order_date, days)
            return days, f"{phrase.replace(' ', '_')}_{days}d", due

    return None, "implicit_null", None

def _add_days(order_date: Optional[str], days: int) -> Optional[str]:
    if not order_date:
        # Use today as reference
        base = datetime.now()
    else:
        try:
            base = datetime.strptime(order_date, '%Y-%m-%d')
        except:
            base = datetime.now()
    return (base + timedelta(days=days)).strftime('%Y-%m-%d')

def detect_department(text: str) -> tuple[str, float]:
    t = text.lower()
    for dept, keywords in DEPT_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in t)
        if matches >= 2:
            return dept, 0.88
        if matches == 1:
            return dept, 0.65
    return "Government of Karnataka", 0.4

def calculate_contempt_risk(days_left: Optional[int]) -> str:
    if days_left is None:
        return "amber"
    if days_left < 0:
        return "critical"
    if days_left <= 7:
        return "critical"
    if days_left <= 15:
        return "red"
    if days_left <= 30:
        return "amber"
    return "green"

def calculate_days_left(due_date: Optional[str]) -> Optional[int]:
    if not due_date:
        return None
    try:
        d = datetime.strptime(due_date, '%Y-%m-%d')
        return (d - datetime.now()).days
    except:
        return None
