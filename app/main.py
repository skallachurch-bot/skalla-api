from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import webhook

app = FastAPI(
    title="SKALLA API",
    version="1.0.0"
)

# CORS (libera chamadas externas se precisar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router do webhook
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])


@app.get("/")
async def root():
    return {"status": "SKALLA API ONLINE 🚀"}
