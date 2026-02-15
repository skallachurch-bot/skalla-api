from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.database import get_db
from app.models import Schedule, Church

router = APIRouter(prefix="/schedules", tags=["schedules"])

class ScheduleCreate(BaseModel):
    church_id: int
    service_date: date

@router.post("/", response_model=dict)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)):
    church = db.query(Church).filter(Church.id == payload.church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="church_not_found")

    s = Schedule(church_id=payload.church_id, service_date=payload.service_date)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "church_id": s.church_id, "service_date": str(s.service_date)}
