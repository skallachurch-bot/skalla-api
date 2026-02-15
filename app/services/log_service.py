from sqlalchemy.orm import Session
from app.models import Log

def create_log(db: Session, level: str, message: str):
    row = Log(level=level, message=message[:500])
    db.add(row)
    db.commit()
    return row
