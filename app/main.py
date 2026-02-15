from fastapi import FastAPI
from app.routers import webhook

app = FastAPI()

# Inclui o webhook com prefixo correto
app.include_router(webhook.router, prefix="/webhook")

@app.get("/")
def root():
    return {"status": "SKALLA API ONLINE 🚀"}
