from fastapi import APIRouter
from app.api.users.users_router import router as users_router
from app.api.datasets.datasets_router import router as datasets_router
from app.api.rags.rags_router import router as rags_router

router = APIRouter()

router.include_router(users_router, prefix="/api/users", tags=["users"])
router.include_router(datasets_router, prefix="/api/datasets", tags=["datasets"])
router.include_router(rags_router, prefix="/api/rags", tags=["rags"])