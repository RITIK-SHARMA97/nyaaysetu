from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Designation(Base):
    __tablename__ = "designations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    level = Column(String, default="officer")  # officer/head/secretary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    officers = relationship("Officer", back_populates="designation")
    action_items = relationship("ActionItem", back_populates="designation")

class Officer(Base):
    __tablename__ = "officers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="officer")
    is_active = Column(Boolean, default=True)
    designation_id = Column(String, ForeignKey("designations.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    designation = relationship("Designation", back_populates="officers")
