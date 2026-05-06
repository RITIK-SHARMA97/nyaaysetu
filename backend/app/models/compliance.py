from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.sql import func
import uuid
from app.database import Base

class ComplianceHealth(Base):
    __tablename__ = "compliance_health"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    department = Column(String, nullable=False, unique=True)
    total_actions = Column(Integer, default=0)
    complied_actions = Column(Integer, default=0)
    overdue_actions = Column(Integer, default=0)
    critical_actions = Column(Integer, default=0)
    compliance_score = Column(Float, default=100.0)
    trend = Column(String, default="stable")  # improving/stable/worsening
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
