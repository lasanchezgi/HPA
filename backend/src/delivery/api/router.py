from fastapi import APIRouter

from src.delivery.api.v1.auth import router as auth_router
from src.delivery.api.v1.coach import router as coach_router
from src.delivery.api.v1.dashboard import router as dashboard_router
from src.delivery.api.v1.habits import router as habits_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(habits_router)
api_router.include_router(dashboard_router)
api_router.include_router(coach_router)
