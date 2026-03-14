from functools import lru_cache

from app.application.services.prompt_builder_service import PromptBuilderService
from app.application.services.tag_detection_service import TagDetectionService
from app.core.config import AppSettings, get_settings
from app.infrastructure.db.repositories.supabase_persona_repository import (
    SupabasePersonaRepository,
)
from app.infrastructure.db.repositories.supabase_project_repository import (
    SupabaseProjectRepository,
)
from app.infrastructure.db.repositories.supabase_reference_prompt_repository import (
    SupabaseReferencePromptRepository,
)
from app.infrastructure.db.repositories.supabase_prompt_repository import (
    SupabasePromptRepository,
)
from app.infrastructure.llm.gemini_gateway import GeminiGateway


def get_app_settings() -> AppSettings:
    return get_settings()


@lru_cache
def get_prompt_repository() -> SupabasePromptRepository:
    return SupabasePromptRepository()


@lru_cache
def get_project_repository() -> SupabaseProjectRepository:
    return SupabaseProjectRepository()


@lru_cache
def get_persona_repository() -> SupabasePersonaRepository:
    return SupabasePersonaRepository()


@lru_cache
def get_reference_prompt_repository() -> SupabaseReferencePromptRepository:
    return SupabaseReferencePromptRepository()


@lru_cache
def get_llm_gateway() -> GeminiGateway:
    return GeminiGateway()


def get_prompt_builder_service() -> PromptBuilderService:
    return PromptBuilderService(tag_detection_service=TagDetectionService())
