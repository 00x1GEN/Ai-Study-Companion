from fastapi import APIRouter
from .auth import router as auth_router
from .courses import router as courses_router
from .learning import router as learning_router
from .ai import router as ai_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(courses_router)
router.include_router(learning_router)
router.include_router(ai_router)
