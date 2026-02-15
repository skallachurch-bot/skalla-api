import requests
from app.settings import settings

def send_whatsapp_message(to_phone: str, text: str) -> dict:
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_NUMBER_ID:
        return {"status": "disabled", "reason": "missing_whatsapp_config"}

    url = f"https://graph.facebook.com/v20.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text},
    }
    r = requests.post(url, headers=headers, json=data, timeout=20)
    try:
        return {"status": "sent", "code": r.status_code, "json": r.json()}
    except Exception:
        return {"status": "sent", "code": r.status_code, "text": r.text}
