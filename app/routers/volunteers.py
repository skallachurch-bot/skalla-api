from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Volunteer, Church

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

class VolunteerCreate(BaseModel):
    church_id: int
    name: str
    phone: str
    is_leader: bool = False

@router.post("/", response_model=dict)
def create_volunteer(payload: VolunteerCreate, db: Session = Depends(get_db)):
    church = db.query(Church).filter(Church.id == payload.church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="church_not_found")

    exists = db.query(Volunteer).filter(
        Volunteer.church_id == payload.church_id,
        Volunteer.phone == payload.phone
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="volunteer_phone_already_exists")

    v = Volunteer(
        church_id=payload.church_id,
        name=payload.name,
        phone=payload.phone,
        is_leader=payload.is_leader,
        is_active=True
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"id": v.id, "church_id": v.church_id, "name": v.name, "phone": v.phone, "is_leader": v.is_leader}
