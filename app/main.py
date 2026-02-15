from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.churches import router as churches_router
from app.routers.volunteers import router as volunteers_router
from app.routers.departments import router as departments_router
from app.routers.schedules import router as schedules_router
from app.routers.schedule_assignments import router as schedule_assignments_router
from app.routers.webhook import router as webhook_router
from app.routers.logs import router as logs_router

app = FastAPI(title="SKALLA API", version="1.0")
app.include_router(health_router)
app.include_router(churches_router)
app.include_router(volunteers_router)
app.include_router(departments_router)
app.include_router(schedules_router)
app.include_router(schedule_assignments_router)
app.include_router(webhook_router)
app.include_router(logs_router)
