
from fastapi.testclient import TestClient

from app.main import app


def test_live_product_search_endpoint():
    client = TestClient(app)

    response = client.post(
        "/api/v1/products/search",
        json={
            "query": "Samsung phone under 30000",
            "max_price": 30000,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "Samsung phone under 30000"
    assert data["total"] <= 5
    assert isinstance(data["products"], list)

    for product in data["products"]:
        assert product["title"]
        assert product["product_url"]
        assert product["source"]


def test_live_search_accepts_natural_language_query(
    monkeypatch,
):
    from app.api.routes.products import (
        get_product_search_service,
    )
    from app.ingestion.providers.mock_search import (
        MockSearchProvider,
    )
    from app.services.product_search_service import (
        ProductSearchService,
    )

    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    monkeypatch.setattr(
        "app.api.routes.products.get_product_search_service",
        lambda: service,
    )

    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    response = client.post(
        "/api/v1/products/search",
        json={
            "query": (
                "Samsung phone under 30000 "
                "with rating 4.5+"
            ),
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["interpreted_query"]["product_query"] == (
        "Samsung phone"
    )

    assert data["interpreted_query"]["max_price"] == 30000

    assert data["interpreted_query"]["min_rating"] == 4.5

    assert data["total"] >= 0

