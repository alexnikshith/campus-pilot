from fastapi import APIRouter
from app.api.v1.routes import health, system, auth, profile, assessment

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(system.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(profile.router)
api_v1_router.include_router(assessment.router)
