from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import requests

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


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

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            text = message["text"]["body"]

            send_message(from_number, f"Recebi: {text}")

    except Exception as e:
        print("ERRO:", e)

    return {"status": "ok"}


def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=data)
    print("RESPOSTA META:", response.text)

