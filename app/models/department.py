from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint
from app.models.base import Base

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = (UniqueConstraint("church_id", "name", name="uq_department_church_name"),)
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
