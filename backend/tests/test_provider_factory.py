from app.ingestion.providers.factory import (
    create_serpapi_provider,
)


def test_factory_creates_serpapi_provider(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.ingestion.providers.factory.settings.serpapi_api_key",
        "factory-test-key",
    )

    provider = create_serpapi_provider()

    assert provider.api_key == "factory-test-key"
