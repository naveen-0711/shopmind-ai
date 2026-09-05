
from app.core.config import Settings


def test_settings_can_load_serpapi_api_key(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERPAPI_API_KEY",
        "test-api-key",
    )

    settings = Settings()

    assert settings.serpapi_api_key == "test-api-key"



def test_settings_default_api_key_is_empty(
    monkeypatch,
):
    monkeypatch.delenv(
        "SERPAPI_API_KEY",
        raising=False,
    )

    settings = Settings(
        _env_file=None,
    )

    assert settings.serpapi_api_key == ""

