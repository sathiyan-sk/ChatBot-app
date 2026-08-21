from __future__ import annotations

from fastapi import APIRouter

from app.api.admin.applications import router as admin_applications_router
from app.api.admin.conversations import router as admin_conversations_router
from app.api.admin.documents import router as admin_documents_router
from app.api.admin.knowledge_bases import router as admin_knowledge_bases_router
from app.api.admin.settings import router as admin_settings_router
from app.api.admin.widgets import router as admin_widgets_router
from app.api.client.chat import router as client_chat_router
from app.api.client.conversations import router as client_conversations_router
from app.api.admin.ingestion import router as admin_ingestion_router
from app.api.admin.conversation_debug import (
    router as admin_conversation_debug_router,
)
from app.api.client.widget import (
    router as client_widget_router,
)
from app.api.system import router as system_router

api_router = APIRouter(prefix="/api")

api_router.include_router(admin_applications_router)
api_router.include_router(admin_knowledge_bases_router)
api_router.include_router(admin_documents_router)
api_router.include_router(admin_ingestion_router)
api_router.include_router(admin_settings_router)
api_router.include_router(admin_conversations_router)
api_router.include_router(client_chat_router)
api_router.include_router(client_conversations_router)
api_router.include_router(
    admin_conversation_debug_router,
)
api_router.include_router(admin_widgets_router)
api_router.include_router(client_widget_router)
api_router.include_router(system_router)