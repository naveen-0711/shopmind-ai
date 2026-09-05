
from app.api.routes.products import (
    get_product_search_service,
)
from app.ingestion.providers.serpapi_search import (
    SerpApiSearchProvider,
)
from app.services.product_search_service import (
    ProductSearchService,
)


def test_search_dependency_creates_search_service(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.ingestion.providers.factory.settings.serpapi_api_key",
        "dependency-test-key",
    )

    service = get_product_search_service()

    assert isinstance(
        service,
        ProductSearchService,
    )

    assert len(service.providers) == 1

    assert isinstance(
        service.providers[0],
        SerpApiSearchProvider,
    )

    assert (
        service.providers[0].api_key
        == "dependency-test-key"
    )

