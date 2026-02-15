from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, String
from app.models.base import Base

class Confirmation(Base):
    __tablename__ = "confirmations"
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    schedule_assignment_id = Column(Integer, ForeignKey("schedule_assignments.id", ondelete="CASCADE"), nullable=False)
    received_text = Column(String(255), nullable=False)
    result_status = Column(String(16), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
