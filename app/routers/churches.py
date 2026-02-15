from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Church

router = APIRouter(prefix="/churches", tags=["churches"])

class ChurchCreate(BaseModel):
    name: str

@router.post("/", response_model=dict)
def create_church(payload: ChurchCreate, db: Session = Depends(get_db)):
    church = Church(name=payload.name, is_active=True)
    db.add(church)
    db.commit()
    db.refresh(church)
    return {"id": church.id, "name": church.name, "is_active": church.is_active}

@router.get("/{church_id}", response_model=dict)
def get_church(church_id: int, db: Session = Depends(get_db)):
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="church_not_found")
    return {"id": church.id, "name": church.name, "is_active": church.is_active}
