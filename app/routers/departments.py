from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Department, Church

router = APIRouter(prefix="/departments", tags=["departments"])

class DepartmentCreate(BaseModel):
    church_id: int
    name: str

@router.post("/", response_model=dict)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    church = db.query(Church).filter(Church.id == payload.church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="church_not_found")

    exists = db.query(Department).filter(
        Department.church_id == payload.church_id,
        Department.name == payload.name
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="department_already_exists")

    d = Department(church_id=payload.church_id, name=payload.name)
    db.add(d)
    db.commit()
    db.refresh(d)
    return {"id": d.id, "church_id": d.church_id, "name": d.name}
