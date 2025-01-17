from fastapi import APIRouter

from .endpoints import auth_router, user_router, audit_router, editor_router, premises_router, templates_router, roles_router, reports_router, categories_router, question_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(user_router, tags=["user"])
router.include_router(audit_router, tags=["audit"])
router.include_router(editor_router, tags=["editor"])
router.include_router(premises_router, tags=["premises"])
router.include_router(templates_router, tags=["templates"])
router.include_router(roles_router, tags=["roles"])
router.include_router(reports_router, tags=["reports"])
router.include_router(categories_router, tags=["categories"])
router.include_router(question_router, tags=["questions"])
