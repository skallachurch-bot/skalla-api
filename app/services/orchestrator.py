from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Volunteer, ScheduleAssignment, Confirmation
from app.services.log_service import create_log

def _normalize_text(text: str) -> str:
    return (text or "").strip().upper()

def handle_incoming_text(db: Session, phone: str, text: str, church_id: int | None = None) -> dict:
    phone = (phone or "").strip()
    t = _normalize_text(text)

    if not phone:
        return {"status": "error", "message": "missing_phone"}

    qv = db.query(Volunteer).filter(Volunteer.phone == phone, Volunteer.is_active == True)  # noqa
    if church_id is not None:
        qv = qv.filter(Volunteer.church_id == church_id)

    volunteer = qv.first()
    if not volunteer:
        create_log(db, "WARNING", f"no_volunteer_found phone={phone} church_id={church_id}")
        return {"status": "error", "message": "no_volunteer_found"}

    qa = db.query(ScheduleAssignment).filter(
        ScheduleAssignment.volunteer_id == volunteer.id,
        ScheduleAssignment.church_id == volunteer.church_id,
        ScheduleAssignment.status == "PENDING",
    ).order_by(desc(ScheduleAssignment.id))

    assignment = qa.first()
    if not assignment:
        create_log(db, "INFO", f"no_assignment_found volunteer_id={volunteer.id} phone={phone}")
        return {"status": "error", "message": "no_assignment_found"}

    if t in ["SIM", "S", "YES"]:
        assignment.status = "CONFIRMED"
        db.add(assignment)
        db.commit()

        conf = Confirmation(
            church_id=assignment.church_id,
            schedule_assignment_id=assignment.id,
            received_text=text,
            result_status="CONFIRMED",
        )
        db.add(conf)
        db.commit()

        return {"status": "success", "action": "confirmed", "assignment_id": assignment.id}

    if t in ["NAO", "NÃO", "N", "NO"]:
        assignment.status = "DECLINED"
        db.add(assignment)
        db.commit()

        conf = Confirmation(
            church_id=assignment.church_id,
            schedule_assignment_id=assignment.id,
            received_text=text,
            result_status="DECLINED",
        )
        db.add(conf)
        db.commit()

        return {"status": "success", "action": "declined", "assignment_id": assignment.id}

    conf = Confirmation(
        church_id=assignment.church_id,
        schedule_assignment_id=assignment.id,
        received_text=text,
        result_status="IGNORED",
    )
    db.add(conf)
    db.commit()

    return {"status": "ok", "action": "ignored", "message": "unknown_intent"}
