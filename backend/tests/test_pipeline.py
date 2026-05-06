import pytest
import uuid
import json
from types import SimpleNamespace
from app.core.config import Settings
from app.pipeline.classifier import classify_sentence, resolve_implicit_deadline, detect_department, calculate_contempt_risk
from app.pipeline.extractor import find_order_section, find_text_location
from app.pipeline.appeal import calculate_appeal_windows
from app.pipeline.affidavit import generate_affidavit
from app.pipeline import llm, extractor
from app.models.case import Judgment
from app.models.action import ActionItem, AppealWindow
from app.workers.processor import process_judgment_task

def test_classify_high_confidence():
    result = classify_sentence("The Secretary is directed to regularise the services within 30 days.")
    assert result["is_directive"] == True
    assert result["tier"] == "HIGH"
    assert result["confidence"] >= 0.9

def test_classify_non_directive():
    result = classify_sentence("This petition has been filed under Article 226 of the Constitution.")
    assert result["is_directive"] == False

def test_deadline_explicit_days():
    days, basis, due = resolve_implicit_deadline("comply within 30 days", "2024-01-01")
    assert days == 30
    assert "30d" in basis
    assert due is not None

def test_deadline_forthwith():
    days, basis, due = resolve_implicit_deadline("The respondent shall forthwith comply.", "2024-01-01")
    assert days == 7
    assert "forthwith" in basis

def test_deadline_expeditiously():
    days, basis, due = resolve_implicit_deadline("must act expeditiously", "2024-01-01")
    assert days == 30

def test_department_detection():
    dept, conf = detect_department("The Commissioner of Revenue and land records department shall comply.")
    assert "Revenue" in dept
    assert conf > 0.5

def test_contempt_risk_critical():
    assert calculate_contempt_risk(-3) == "critical"
    assert calculate_contempt_risk(3) == "critical"

def test_contempt_risk_green():
    assert calculate_contempt_risk(60) == "green"

def test_appeal_windows():
    windows = calculate_appeal_windows("2024-01-01")
    assert len(windows) == 3
    types = [w["appeal_type"] for w in windows]
    assert "writ_appeal" in types
    assert "slp" in types

def test_affidavit_generation():
    action = {
        "directive_text": "Secretary is directed to regularise services within 30 days.",
        "responsible_designation": "Secretary, Revenue Department",
        "responsible_department": "Revenue Department",
        "judgment_case_number": "WP/45821/2024",
        "order_date": "2024-01-15",
    }
    officer = {"name": "Ravi Kumar", "email": "officer@karnataka.gov"}
    text = generate_affidavit(action, officer)
    assert "WP/45821/2024" in text
    assert "Ravi Kumar" in text
    assert "COMPLIANCE AFFIDAVIT" in text

def test_default_gemini_model_is_supported_alias():
    settings = Settings()
    assert settings.GEMINI_MODEL == "gemini-flash-latest"

def test_find_order_section_ignores_footer_order_mentions():
    pages = [
        {
            "page_num": 1,
            "text": "IN THE HIGH COURT...\nORDER\nPage 1 of 3\nKarnataka High Court - Official Order\n",
        },
        {
            "page_num": 2,
            "text": (
                "Background facts.\n"
                "ACCORDINGLY, the writ petition is allowed and the following directions are issued:\n"
                "i. The Commissioner, BBMP, is hereby directed to remove the illegal encroachments forthwith.\n"
                "ii. Respondent No. 3 shall submit a compliance report within four weeks.\n"
            ),
        },
        {
            "page_num": 3,
            "text": "Matter listed for compliance.\nPage 3 of 3\nKarnataka High Court - Official Order\n",
        },
    ]

    order_text, start_page = find_order_section(pages)

    assert start_page == 2
    assert "following directions are issued" in order_text
    assert "remove the illegal encroachments" in order_text
    assert "Official Order" not in order_text

def test_extract_actions_falls_back_when_model_returns_empty(monkeypatch):
    expected = [{
        "directive_text": "The Commissioner, BBMP is hereby directed to remove the encroachment forthwith.",
        "responsible_designation": "Commissioner, BBMP",
        "responsible_department": "Urban Development",
        "action_type": "compliance",
        "due_date_text": "forthwith",
        "source_sentence": "The Commissioner, BBMP is hereby directed to remove the encroachment forthwith.",
        "confidence": 0.88,
    }]

    class DummyResponse:
        text = "[]"

    class DummyModels:
        @staticmethod
        def generate_content(*args, **kwargs):
            return DummyResponse()

    class DummyClient:
        def __init__(self, *args, **kwargs):
            self.models = DummyModels()

    monkeypatch.setattr(llm, "USE_NEW_SDK", True)
    monkeypatch.setattr(llm, "genai", SimpleNamespace(Client=DummyClient))
    monkeypatch.setattr(llm, "_fallback_extraction", lambda text: expected)

    result = llm.extract_actions_from_text(
        "The Commissioner, BBMP is hereby directed to remove the encroachment forthwith."
    )

    assert result == expected

def test_find_text_location_returns_bbox_for_matching_sentence():
    pages = [{
        "page_num": 2,
        "words": [
            (10.0, 20.0, 42.0, 30.0, "The"),
            (45.0, 20.0, 105.0, 30.0, "Commissioner,"),
            (108.0, 20.0, 150.0, 30.0, "BBMP"),
            (153.0, 20.0, 165.0, 30.0, "is"),
            (168.0, 20.0, 220.0, 30.0, "hereby"),
            (223.0, 20.0, 290.0, 30.0, "directed"),
        ],
    }]

    page_num, bbox = find_text_location(
        pages,
        "The Commissioner BBMP is hereby directed to remove encroachment"
    )

    assert page_num == 2
    assert bbox == [10.0, 20.0, 290.0, 30.0]

def test_process_judgment_persists_source_bbox_for_fresh_upload(test_db, monkeypatch):
    test_db.query(AppealWindow).delete()
    test_db.query(ActionItem).delete()
    test_db.query(Judgment).delete()
    test_db.commit()

    judgment = Judgment(
        id=str(uuid.uuid4()),
        pdf_path="uploads/fresh-upload.pdf",
        pdf_filename="fresh-upload.pdf",
        processing_status="pending",
        progress=0,
    )
    test_db.add(judgment)
    test_db.commit()

    pages = [
        {"page_num": 1, "text": "Intro", "words": [], "is_scanned": False, "char_count": 5},
        {
            "page_num": 2,
            "text": "The Commissioner, BBMP is hereby directed to remove the illegal encroachments forthwith.",
            "words": [
                (10.0, 20.0, 42.0, 30.0, "The"),
                (45.0, 20.0, 105.0, 30.0, "Commissioner,"),
                (108.0, 20.0, 150.0, 30.0, "BBMP"),
                (153.0, 20.0, 165.0, 30.0, "is"),
                (168.0, 20.0, 220.0, 30.0, "hereby"),
                (223.0, 20.0, 290.0, 30.0, "directed"),
            ],
            "is_scanned": False,
            "char_count": 86,
        },
    ]
    raw_actions = [{
        "directive_text": "The Commissioner, BBMP is hereby directed to remove the illegal encroachments forthwith.",
        "responsible_designation": "Commissioner, BBMP",
        "responsible_department": "Urban Development",
        "action_type": "compliance",
        "due_date_text": "forthwith",
        "source_sentence": "The Commissioner, BBMP is hereby directed to remove the illegal encroachments forthwith.",
        "confidence": 0.91,
    }]

    monkeypatch.setattr(extractor, "extract_pages", lambda path: pages)
    monkeypatch.setattr(extractor, "get_pdf_metadata", lambda path: {"total_pages": 2, "title": "", "author": ""})
    monkeypatch.setattr(extractor, "detect_page_type", lambda text: "digital")
    monkeypatch.setattr(extractor, "find_order_section", lambda extracted_pages: (pages[1]["text"], 2))
    monkeypatch.setattr(llm, "extract_actions_from_text", lambda *args, **kwargs: raw_actions)

    process_judgment_task(judgment.id, judgment.pdf_path, test_db)

    saved = test_db.query(ActionItem).filter(ActionItem.judgment_id == judgment.id).one()
    assert saved.source_page == 2
    assert json.loads(saved.source_bbox) == [10.0, 20.0, 290.0, 30.0]
