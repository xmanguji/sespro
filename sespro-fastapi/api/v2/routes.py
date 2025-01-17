from fastapi import APIRouter

from .endpoints import editor_router

router = APIRouter()
router.include_router(editor_router, tags=["editor v2"])
