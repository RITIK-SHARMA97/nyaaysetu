from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    action_item_id = Column(String, ForeignKey("action_items.id"), nullable=False)
    officer_email = Column(String, nullable=False)
    officer_name = Column(String)
    event_type = Column(String, nullable=False)  # approved/edited/rejected/status_changed/escalated
    old_value = Column(Text)
    new_value = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    action_item = relationship("ActionItem", back_populates="audit_logs")
