from sqlalchemy import Column, Integer, DateTime, func, String
from app.models.base import Base

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(16), nullable=False, default="INFO")
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
