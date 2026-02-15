from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.models.base import Base

class Church(Base):
    __tablename__ = "churches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
