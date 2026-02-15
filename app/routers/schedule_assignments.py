from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import ScheduleAssignment, Schedule, Volunteer, Department

router = APIRouter(prefix="/schedule-assignments", tags=["schedule-assignments"])

class AssignmentCreate(BaseModel):
    church_id: int
    schedule_id: int
    volunteer_id: int
    department_id: int

@router.post("/", response_model=dict)
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == payload.schedule_id, Schedule.church_id == payload.church_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule_not_found_for_church")

    volunteer = db.query(Volunteer).filter(Volunteer.id == payload.volunteer_id, Volunteer.church_id == payload.church_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="volunteer_not_found_for_church")

    dept = db.query(Department).filter(Department.id == payload.department_id, Department.church_id == payload.church_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="department_not_found_for_church")

    a = ScheduleAssignment(
        church_id=payload.church_id,
        schedule_id=payload.schedule_id,
        volunteer_id=payload.volunteer_id,
        department_id=payload.department_id,
        status="PENDING",
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id, "status": a.status}
