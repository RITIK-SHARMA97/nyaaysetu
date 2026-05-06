import uuid
import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.case import Judgment
from app.models.action import ActionItem, AppealWindow
from app.models.compliance import ComplianceHealth
from app.pipeline import extractor, llm, deadline, appeal

def process_judgment_task(judgment_id: str, pdf_path: str, db: Session | None = None):
    """Full pipeline: PDF → extracted action items saved to DB."""
    owns_session = db is None
    if db is None:
        db = SessionLocal()

    j = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not j:
        if owns_session:
            db.close()
        return

    try:
        # Step 1: Extract text from PDF
        _update_status(j, db, "extracting", 10)
        pages = extractor.extract_pages(pdf_path)
        meta = extractor.get_pdf_metadata(pdf_path)
        j.total_pages = meta["total_pages"]

        # Step 2: Check for Kannada pages
        _update_status(j, db, "ocr", 25)
        has_kannada = any(extractor.detect_page_type(p["text"]) == "kannada" for p in pages)
        j.has_kannada = str(has_kannada).lower()

        # Step 3: Find ORDER section
        _update_status(j, db, "classifying", 40)
        order_text, start_page = extractor.find_order_section(pages)
        j.order_section = order_text

        # Step 4: LLM extraction
        _update_status(j, db, "llm", 60)
        raw_actions = llm.extract_actions_from_text(
            order_text,
            case_id=j.case_number or "UNKNOWN",
            order_date=j.order_date or ""
        )

        # Step 5: Enrich with deadlines and contempt risk
        _update_status(j, db, "enriching", 80)
        enriched_actions = deadline.enrich_actions(raw_actions, j.order_date)

        # Step 6: Save action items
        for action_data in enriched_actions:
            dept = action_data.get("responsible_department", "Government of Karnataka")
            conf = float(action_data.get("confidence", 0.8))
            source_text = action_data.get("source_sentence") or action_data.get("directive_text", "")
            source_page, source_bbox = extractor.find_text_location(pages, source_text, preferred_page=start_page)
            item = ActionItem(
                id=str(uuid.uuid4()),
                judgment_id=judgment_id,
                directive_text=action_data.get("directive_text", ""),
                source_page=source_page or start_page,
                source_bbox=json.dumps(source_bbox) if source_bbox else None,
                source_sentence=action_data.get("source_sentence", ""),
                action_type=action_data.get("action_type", "compliance"),
                responsible_designation=action_data.get("responsible_designation", ""),
                responsible_department=dept,
                due_date=action_data.get("due_date"),
                due_date_basis=action_data.get("due_date_basis", "implicit_null"),
                days_left=action_data.get("days_left"),
                contempt_risk=action_data.get("contempt_risk", "amber"),
                confidence_overall=conf,
                confidence_directive=min(conf + 0.05, 1.0),
                confidence_department=conf - 0.1 if conf > 0.1 else conf,
                confidence_deadline=conf - 0.05 if conf > 0.05 else conf,
                status="new"
            )
            db.add(item)
            _update_compliance_health(db, dept)

        # Step 7: Appeal windows
        appeal_windows = appeal.calculate_appeal_windows(j.order_date)
        for w in appeal_windows:
            aw = AppealWindow(
                id=str(uuid.uuid4()),
                judgment_id=judgment_id,
                **w
            )
            db.add(aw)

        _update_status(j, db, "ready", 100)

    except Exception as e:
        j.processing_status = "failed"
        j.error_message = str(e)
        db.commit()
        raise e
    finally:
        if owns_session:
            db.close()

def _update_status(judgment, db, status, progress):
    judgment.processing_status = status
    judgment.progress = progress
    db.commit()

def _update_compliance_health(db, department):
    ch = db.query(ComplianceHealth).filter(ComplianceHealth.department == department).first()
    if not ch:
        ch = ComplianceHealth(id=str(uuid.uuid4()), department=department)
        db.add(ch)
    ch.total_actions = (ch.total_actions or 0) + 1
    db.commit()
