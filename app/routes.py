from fastapi import APIRouter

from app.routes_auth import router as auth_router
from app.routes_admin import router as admin_router
from app.routes_public import router as public_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(public_router)