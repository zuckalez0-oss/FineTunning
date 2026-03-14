import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


def _load_environment() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    workspace_root = backend_root.parent

    load_dotenv(workspace_root / ".env", override=False)
    load_dotenv(backend_root / ".env", override=True)


@dataclass(frozen=True)
class AppSettings:
    project_name: str
    version: str
    api_v1_prefix: str
    environment: str
    allowed_origins: list[str]
    supabase_url: str
    supabase_service_role_key: str
    gemini_api_key: str
    default_llm_model: str


@lru_cache
def get_settings() -> AppSettings:
    _load_environment()

    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    return AppSettings(
        project_name=os.getenv("PROJECT_NAME", "PromptMaster API"),
        version=os.getenv("APP_VERSION", "1.0.0"),
        api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
        environment=os.getenv("ENVIRONMENT", "development"),
        allowed_origins=[origin.strip() for origin in origins.split(",") if origin.strip()],
        supabase_url=os.getenv("SUPABASE_URL", "").strip(),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip(),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        default_llm_model=os.getenv("DEFAULT_LLM_MODEL", "gemini-2.5-flash"),
    )
