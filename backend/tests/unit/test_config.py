from app.core.config import get_settings


def test_settings_expose_default_api_prefix() -> None:
    settings = get_settings()
    assert settings.api_v1_prefix.startswith("/api/")
