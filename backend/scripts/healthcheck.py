from app.core.config import get_settings


def main() -> None:
    settings = get_settings()
    print(
        {
            "project": settings.project_name,
            "environment": settings.environment,
            "supabase_configured": bool(
                settings.supabase_url and settings.supabase_service_role_key
            ),
            "gemini_configured": bool(settings.gemini_api_key),
        }
    )


if __name__ == "__main__":
    main()
