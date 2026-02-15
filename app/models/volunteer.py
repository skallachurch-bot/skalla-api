from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint, Boolean
from app.models.base import Base

class Volunteer(Base):
    __tablename__ = "volunteers"
    __table_args__ = (UniqueConstraint("church_id", "phone", name="uq_volunteer_church_phone"),)
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(120), nullable=False)
    phone = Column(String(32), nullable=False)
    is_leader = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
