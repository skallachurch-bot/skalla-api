from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@router.get("/")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return JSONResponse(content=int(challenge))

    raise HTTPException(status_code=403, detail="verification_failed")


@router.post("/")
async def webhook(request: Request):
    body = await request.json()

    print("==== WEBHOOK RECEBIDO ====")
    print(body)
    print("==========================")

    return {"status": "ok"}
