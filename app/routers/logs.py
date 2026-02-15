from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Log

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/", response_model=list[dict])
def list_logs(db: Session = Depends(get_db)):
    rows = db.query(Log).order_by(Log.id.desc()).limit(200).all()
    return [{"id": r.id, "level": r.level, "message": r.message, "created_at": str(r.created_at)} for r in rows]
