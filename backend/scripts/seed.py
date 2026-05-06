"""Seed database with realistic Karnataka HC data for demo."""
import sys, os, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_tables
from app.models.case import Judgment
from app.models.action import ActionItem, ActionChain, AppealWindow
from app.models.audit import AuditLog
from app.models.officer import Designation, Officer
from app.models.compliance import ComplianceHealth
from datetime import datetime, timedelta

def seed():
    create_tables()
    db = SessionLocal()

    # Clear existing seed data
    db.query(AuditLog).delete()
    db.query(ActionChain).delete()
    db.query(AppealWindow).delete()
    db.query(ActionItem).delete()
    db.query(Judgment).delete()
    db.query(ComplianceHealth).delete()
    db.query(Officer).delete()
    db.query(Designation).delete()
    db.commit()

    # Designations
    d1 = Designation(id=str(uuid.uuid4()), title="Secretary, Revenue Department", department="Revenue Department", level="secretary")
    d2 = Designation(id=str(uuid.uuid4()), title="Commissioner, Urban Development", department="Urban Development", level="head")
    d3 = Designation(id=str(uuid.uuid4()), title="Director, Education Department", department="Education Department", level="head")
    for d in [d1, d2, d3]:
        db.add(d)
    db.flush()

    # Officers
    officers_data = [
        Officer(id=str(uuid.uuid4()), email="officer@karnataka.gov", name="Ravi Kumar", role="officer", designation_id=d1.id),
        Officer(id=str(uuid.uuid4()), email="head@karnataka.gov", name="Suresh Nair", role="head", designation_id=d1.id),
        Officer(id=str(uuid.uuid4()), email="new_officer@karnataka.gov", name="Amit Patel", role="officer", designation_id=d2.id),
    ]
    for o in officers_data:
        db.add(o)

    now = datetime.now()

    # Judgment 1 — Revenue case (critical)
    j1 = Judgment(
        id=str(uuid.uuid4()),
        case_number="WP/45821/2024",
        order_date="2024-01-15",
        pdf_filename="WP_45821_2024_Revenue.pdf",
        processing_status="ready",
        progress=100,
        total_pages=18,
        has_kannada="false"
    )
    db.add(j1)
    db.flush()

    actions_j1 = [
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j1.id, designation_id=d1.id,
            directive_text="The Secretary, Revenue Department is directed to regularise the services of the petitioner within 30 days from the date of this order.",
            source_page=16, source_sentence="The Secretary, Revenue Department is directed to regularise the services of the petitioner within 30 days from the date of this order.",
            action_type="regularisation", responsible_designation="Secretary, Revenue Department",
            responsible_department="Revenue Department",
            due_date=(now - timedelta(days=3)).strftime('%Y-%m-%d'),
            due_date_basis="explicit_30d", days_left=-3, contempt_risk="critical",
            confidence_overall=0.95, confidence_directive=0.97, confidence_department=0.90, confidence_deadline=0.96,
            status="in_progress", is_escalated=True
        ),
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j1.id, designation_id=d1.id,
            directive_text="The respondent shall file a compliance report before this Court within 6 weeks.",
            source_page=17, source_sentence="The respondent shall file a compliance report before this Court within 6 weeks.",
            action_type="report", responsible_designation="Secretary, Revenue Department",
            responsible_department="Revenue Department",
            due_date=(now + timedelta(days=4)).strftime('%Y-%m-%d'),
            due_date_basis="explicit_42d", days_left=4, contempt_risk="critical",
            confidence_overall=0.91, confidence_directive=0.95, confidence_department=0.88, confidence_deadline=0.93,
            status="approved"
        ),
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j1.id, designation_id=d1.id,
            directive_text="The Tahsildar, Bengaluru North Taluk, shall file a compliance affidavit before this Court after implementing the regularisation order.",
            source_page=17, source_sentence="The Tahsildar, Bengaluru North Taluk, shall file a compliance affidavit before this Court after implementing the regularisation order.",
            action_type="report", responsible_designation="Secretary, Revenue Department",
            responsible_department="Revenue Department",
            due_date=(now + timedelta(days=10)).strftime('%Y-%m-%d'),
            due_date_basis="post_compliance_affidavit", days_left=10, contempt_risk="red",
            confidence_overall=0.89, confidence_directive=0.92, confidence_department=0.86, confidence_deadline=0.84,
            status="complied"
        ),
    ]

    # Judgment 2 — Urban Development (amber)
    j2 = Judgment(
        id=str(uuid.uuid4()),
        case_number="WP/12334/2024",
        order_date="2024-02-20",
        pdf_filename="WP_12334_2024_Urban.pdf",
        processing_status="ready", progress=100, total_pages=12, has_kannada="false"
    )
    db.add(j2)
    db.flush()

    actions_j2 = [
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j2.id, designation_id=d2.id,
            directive_text="The Commissioner, BBMP is hereby directed to remove the illegal encroachments on survey number 142 forthwith.",
            source_page=10, source_sentence="The Commissioner, BBMP is hereby directed to remove the illegal encroachments on survey number 142 forthwith.",
            action_type="compliance", responsible_designation="Commissioner, Urban Development",
            responsible_department="Urban Development",
            due_date=(now + timedelta(days=20)).strftime('%Y-%m-%d'),
            due_date_basis="forthwith_7d", days_left=20, contempt_risk="amber",
            confidence_overall=0.88, confidence_directive=0.92, confidence_department=0.85, confidence_deadline=0.80,
            status="assigned"
        ),
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j2.id, designation_id=d2.id,
            directive_text="The respondent authority shall issue the occupancy certificate to the petitioner at the earliest.",
            source_page=11,
            action_type="compliance", responsible_designation="Commissioner, Urban Development",
            responsible_department="Urban Development",
            due_date=(now + timedelta(days=25)).strftime('%Y-%m-%d'),
            due_date_basis="earliest_14d", days_left=25, contempt_risk="amber",
            confidence_overall=0.84, confidence_directive=0.89, confidence_department=0.82, confidence_deadline=0.78,
            status="new"
        ),
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j2.id, designation_id=d2.id,
            directive_text="The Assistant Revenue Officer, R.M.V. Ward, BBMP, shall place the compliance affidavit on record after completing the demolition exercise.",
            source_page=11,
            source_sentence="The Assistant Revenue Officer, R.M.V. Ward, BBMP, shall place the compliance affidavit on record after completing the demolition exercise.",
            action_type="report", responsible_designation="Commissioner, Urban Development",
            responsible_department="Urban Development",
            due_date=(now + timedelta(days=12)).strftime('%Y-%m-%d'),
            due_date_basis="post_demolition_affidavit", days_left=12, contempt_risk="red",
            confidence_overall=0.86, confidence_directive=0.90, confidence_department=0.84, confidence_deadline=0.82,
            status="complied"
        ),
    ]

    # Judgment 3 — Education (green)
    j3 = Judgment(
        id=str(uuid.uuid4()),
        case_number="WP/67890/2023",
        order_date="2023-11-10",
        pdf_filename="WP_67890_2023_Education.pdf",
        processing_status="ready", progress=100, total_pages=22, has_kannada="false"
    )
    db.add(j3)
    db.flush()

    actions_j3 = [
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j3.id, designation_id=d3.id,
            directive_text="The Director of Public Instruction shall ensure that all government school teachers are paid their pending salaries within 45 days.",
            source_page=19,
            action_type="payment", responsible_designation="Director, Education Department",
            responsible_department="Education Department",
            due_date=(now + timedelta(days=45)).strftime('%Y-%m-%d'),
            due_date_basis="explicit_45d", days_left=45, contempt_risk="green",
            confidence_overall=0.92, confidence_directive=0.94, confidence_department=0.91, confidence_deadline=0.95,
            status="complied"
        ),
        ActionItem(
            id=str(uuid.uuid4()), judgment_id=j3.id, designation_id=d3.id,
            directive_text="A status report must be filed before this Court after completion of payment.",
            source_page=20,
            action_type="report", responsible_designation="Director, Education Department",
            responsible_department="Education Department",
            due_date=(now + timedelta(days=60)).strftime('%Y-%m-%d'),
            due_date_basis="explicit_60d", days_left=60, contempt_risk="green",
            confidence_overall=0.87, confidence_directive=0.90, confidence_department=0.85, confidence_deadline=0.88,
            status="verified"
        ),
    ]

    for action in actions_j1 + actions_j2 + actions_j3:
        db.add(action)

    # Appeal windows for j1
    for aw_data in [
        {"appeal_type": "writ_appeal", "window_days": 30, "deadline_date": (now + timedelta(days=5)).strftime('%Y-%m-%d'), "days_remaining": 5, "legal_basis": "Order 41 Rule 1, CPC"},
        {"appeal_type": "slp", "window_days": 90, "deadline_date": (now + timedelta(days=65)).strftime('%Y-%m-%d'), "days_remaining": 65, "legal_basis": "Article 136, Constitution"},
    ]:
        db.add(AppealWindow(id=str(uuid.uuid4()), judgment_id=j1.id, **aw_data))

    # Compliance health
    depts = [
        ComplianceHealth(id=str(uuid.uuid4()), department="Revenue Department", total_actions=3, complied_actions=1, overdue_actions=1, critical_actions=2, compliance_score=34.0, trend="worsening"),
        ComplianceHealth(id=str(uuid.uuid4()), department="Urban Development", total_actions=3, complied_actions=1, overdue_actions=0, critical_actions=0, compliance_score=61.0, trend="stable"),
        ComplianceHealth(id=str(uuid.uuid4()), department="Education Department", total_actions=2, complied_actions=2, overdue_actions=0, critical_actions=0, compliance_score=100.0, trend="improving"),
    ]
    for ch in depts:
        db.add(ch)

    db.commit()
    db.close()
    print("✅ Database seeded with 3 Karnataka HC cases, 6 actions, 3 departments")

if __name__ == "__main__":
    seed()
