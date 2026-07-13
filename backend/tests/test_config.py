from app.core.config import Settings


def test_settings_parse_comma_separated_cors_origins() -> None:
    settings = Settings(cors_allowed_origins=("http://localhost:5173,http://localhost:4173"))

    assert settings.cors_allowed_origins == [
        "http://localhost:5173",
        "http://localhost:4173",
    ]


def test_settings_use_expected_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "SentinelAI API"
    assert settings.app_version == "0.1.0"
    assert settings.app_env == "development"
    assert settings.api_v1_prefix == "/api/v1"
