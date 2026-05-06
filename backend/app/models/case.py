from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_number = Column(String, unique=True, nullable=False)
    case_type = Column(String, default="WP")  # WP/SLP/LP/Civil
    petitioner = Column(String)
    respondent = Column(String)
    court = Column(String, default="Karnataka High Court")
    bench = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    judgments = relationship("Judgment", back_populates="case")

class Judgment(Base):
    __tablename__ = "judgments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"), nullable=True)
    case_number = Column(String)
    order_date = Column(String)
    pdf_path = Column(String)
    pdf_filename = Column(String)
    processing_status = Column(String, default="pending")  # pending/extracting/ocr/classifying/llm/enriching/ready/failed
    progress = Column(Integer, default=0)
    raw_text = Column(Text)
    order_section = Column(Text)
    total_pages = Column(Integer, default=0)
    has_kannada = Column(String, default="false")
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    case = relationship("Case", back_populates="judgments")
    action_items = relationship("ActionItem", back_populates="judgment")
    appeal_windows = relationship("AppealWindow", back_populates="judgment")
