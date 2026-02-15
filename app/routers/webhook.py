from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.settings import settings
from app.services.orchestrator import handle_incoming_text
from app.services.log_service import create_log

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.get("/")
def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN and challenge:
        return int(challenge)

    raise HTTPException(status_code=403, detail="verification_failed")

@router.post("/")
async def webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    # WhatsApp Cloud API payload
    if isinstance(payload, dict) and payload.get("entry"):
        try:
            entries = payload.get("entry", [])
            for e in entries:
                changes = e.get("changes", [])
                for c in changes:
                    value = c.get("value", {})
                    messages = value.get("messages", []) or []
                    for m in messages:
                        from_phone = m.get("from", "")
                        text = (m.get("text", {}) or {}).get("body", "") or ""
                        result = handle_incoming_text(db=db, phone=from_phone, text=text)
                        create_log(db, "INFO", f"whatsapp handled phone={from_phone} result={result}")
            return {"status": "ok"}
        except Exception as ex:
            create_log(db, "ERROR", f"webhook_meta_parse_error: {ex}")
            raise

    # Test payload (PowerShell)
    if isinstance(payload, dict) and "church_id" in payload and "phone" in payload and "text" in payload:
        church_id = int(payload["church_id"])
        phone = str(payload["phone"])
        text = str(payload["text"])
        result = handle_incoming_text(db=db, church_id=church_id, phone=phone, text=text)
        return result

    raise HTTPException(status_code=422, detail="invalid_webhook_payload")
