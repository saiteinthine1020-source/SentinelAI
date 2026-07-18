from fastapi import APIRouter

from app.api.routes import auth, health

root_router = APIRouter()
root_router.include_router(health.router)

api_v1_router = APIRouter()
api_v1_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)
