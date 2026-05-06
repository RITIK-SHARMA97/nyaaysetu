from sqlalchemy import Column, String, DateTime, Text, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class ActionItem(Base):
    __tablename__ = "action_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    judgment_id = Column(String, ForeignKey("judgments.id"), nullable=False)
    designation_id = Column(String, ForeignKey("designations.id"), nullable=True)

    # Extracted content
    directive_text = Column(Text, nullable=False)
    source_page = Column(Integer, default=1)
    source_bbox = Column(String)  # JSON: [x0,y0,x1,y1]
    source_sentence = Column(Text)

    # Classification
    action_type = Column(String, default="compliance")
    responsible_designation = Column(String)
    responsible_department = Column(String)

    # Deadline
    due_date = Column(String)
    due_date_basis = Column(String, default="implicit_null")
    days_left = Column(Integer)

    # Risk
    contempt_risk = Column(String, default="green")  # green/amber/red/critical

    # Confidence scores (stored as floats)
    confidence_overall = Column(Float, default=0.8)
    confidence_directive = Column(Float, default=0.8)
    confidence_department = Column(Float, default=0.8)
    confidence_deadline = Column(Float, default=0.8)

    # Workflow
    status = Column(String, default="new")
    is_escalated = Column(Boolean, default=False)
    chain_next = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    judgment = relationship("Judgment", back_populates="action_items")
    designation = relationship("Designation", back_populates="action_items")
    audit_logs = relationship("AuditLog", back_populates="action_item")

class ActionChain(Base):
    __tablename__ = "action_chains"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_action_id = Column(String, ForeignKey("action_items.id"))
    child_action_id = Column(String, ForeignKey("action_items.id"))
    chain_type = Column(String, default="sequential")

class AppealWindow(Base):
    __tablename__ = "appeal_windows"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    judgment_id = Column(String, ForeignKey("judgments.id"), nullable=False)
    appeal_type = Column(String)  # writ_appeal/slp/lp_appeal
    window_days = Column(Integer)
    deadline_date = Column(String)
    days_remaining = Column(Integer)
    legal_basis = Column(String)
    judgment = relationship("Judgment", back_populates="appeal_windows")
