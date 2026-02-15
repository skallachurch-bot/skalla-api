from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, String, UniqueConstraint
from app.models.base import Base

class ScheduleAssignment(Base):
    __tablename__ = "schedule_assignments"
    __table_args__ = (UniqueConstraint("schedule_id", "volunteer_id", "department_id", name="uq_assignment_unique"),)
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(16), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
