from fastapi.testclient import TestClient

from app.api.routes.products import (
    get_product_search_service,
)
from app.ingestion.providers.mock_search import (
    MockSearchProvider,
)
from app.main import app
from app.services.product_search_service import (
    ProductSearchService,
)


class FakeSearchService:
    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ):
        from app.schemas.product import Product

        return [
            Product(
                title="Samsung Galaxy A56",
                price=29999,
                rating=4.5,
                review_count=1250,
                image_url="https://example.com/a56.jpg",
                product_url="https://example.com/a56",
                source="Amazon.in",
                currency="INR",
            )
        ][:limit]


def test_product_search_api():
    app.dependency_overrides[
        get_product_search_service
    ] = lambda: FakeSearchService()

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/products/search",
            json={
                "query": "Samsung phone",
                "max_price": 30000,
                "limit": 10,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["query"] == "Samsung phone"
        assert data["total"] == 1
        assert data["products"][0]["title"] == (
            "Samsung Galaxy A56"
        )

    finally:
        app.dependency_overrides.clear()


def test_product_search_api_accepts_natural_language_query():
    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    app.dependency_overrides[
        get_product_search_service
    ] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/products/search",
            json={
                "query": (
                    "gaming laptop under 70000 "
                    "with rating 4.5+"
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["query"] == (
            "gaming laptop under 70000 "
            "with rating 4.5+"
        )

        assert data["total"] > 0

        for product in data["products"]:
            assert product["price"] is not None
            assert product["price"] <= 70000

            assert product["rating"] is not None
            assert product["rating"] >= 4.5

    finally:
        app.dependency_overrides.clear()


def test_product_search_api_returns_interpreted_query():
    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    app.dependency_overrides[
        get_product_search_service
    ] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/products/search",
            json={
                "query": (
                    "Samsung phone under 30000 "
                    "with rating 4.5+"
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["interpreted_query"]["product_query"] == (
            "Samsung phone"
        )

        assert data["interpreted_query"]["max_price"] == 30000

        assert data["interpreted_query"]["min_rating"] == 4.5

    finally:
        app.dependency_overrides.clear()
