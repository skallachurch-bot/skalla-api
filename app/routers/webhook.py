from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import os
import json

router = APIRouter()

# Token de verificação do Meta
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


# ==============================
# 🔹 VERIFICAÇÃO DO META (GET)
# ==============================
@router.get("/", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge  # Meta exige retorno puro

    raise HTTPException(status_code=403, detail="verification_failed")


# ==============================
# 🔹 RECEBER MENSAGEM (POST)
# ==============================
@router.post("/")
async def receive_message(request: Request):
    body = await request.json()

    print("\n========== WEBHOOK RECEBIDO ==========")
    print(json.dumps(body, indent=2))
    print("======================================")

    try:
        # Verifica se existe mensagem
        if (
            "entry" in body
            and body["entry"]
            and "changes" in body["entry"][0]
            and body["entry"][0]["changes"]
            and "messages" in body["entry"][0]["changes"][0]["value"]
        ):

            message = body["entry"][0]["changes"][0]["value"]["messages"][0]

            numero = message.get("from")
            texto = message.get("text", {}).get("body")

            print(f"\n📱 NUMERO: {numero}")
            print(f"💬 TEXTO: {texto}")

    except Exception as e:
        print("Erro ao processar mensagem:")
        print(e)

    return {"status": "ok"}
