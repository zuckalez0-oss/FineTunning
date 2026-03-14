from fastapi import APIRouter, Depends

from app.api.dependencies import get_app_settings
from app.core.config import AppSettings


router = APIRouter()


@router.get("/")
def healthcheck(settings: AppSettings = Depends(get_app_settings)) -> dict[str, object]:
    return {
        "status": "ok",
        "service": settings.project_name,
        "version": settings.version,
        "environment": settings.environment,
        "checks": {
            "supabase_configured": bool(
                settings.supabase_url and settings.supabase_service_role_key
            ),
            "gemini_configured": bool(settings.gemini_api_key),
        },
    }
