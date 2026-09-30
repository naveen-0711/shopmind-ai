from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_search_response_contains_recommendation_explanation(
    monkeypatch,
):
    from app.schemas.product import Product

    async def fake_search(
        self,
        query,
        max_price=None,
        min_rating=None,
        limit=10,
    ):
        return [
            Product(
                title="Samsung Galaxy A36 5G",
                price=28999,
                currency="INR",
                rating=4.8,
                review_count=8000,
                image_url=None,
                product_url="https://example.com/a36",
                source="Samsung.com",
                lowest_price=28000,
                average_price=32000,
                deal_status="Great Deal",
            )
        ]

    monkeypatch.setattr(
        "app.services.product_search_service.ProductSearchService.search",
        fake_search,
    )

    response = client.post(
        "/api/v1/products/search",
        json={
            "query": "Samsung Galaxy A36",
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["products"]) == 1

    product = data["products"][0]

    assert "recommendation_score" in product
    assert "recommendation_reasons" in product

    assert isinstance(
        product["recommendation_score"],
        (int, float),
    )

    assert isinstance(
        product["recommendation_reasons"],
        list,
    )

    assert len(product["recommendation_reasons"]) > 0

def test_product_search_returns_comparison_summary(
    monkeypatch,
):
    from fastapi.testclient import TestClient

    from app.main import app
    from app.schemas.product import Product

    async def fake_search(self, *args, **kwargs):
        return [
            Product(
                title="Laptop A",
                price=60000,
                currency="INR",
                rating=4.5,
                review_count=1000,
                image_url=None,
                product_url="https://example.com/a",
                source="test",
                lowest_price=None,
                average_price=None,
                deal_status="Good Deal",
            ),
            Product(
                title="Laptop B",
                price=70000,
                currency="INR",
                rating=4.8,
                review_count=5000,
                image_url=None,
                product_url="https://example.com/b",
                source="test",
                lowest_price=None,
                average_price=None,
                deal_status="Great Deal",
            ),
        ]

    from app.services.product_search_service import ProductSearchService

    monkeypatch.setattr(
        ProductSearchService,
        "search",
        fake_search,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/products/search",
        json={
            "query": "gaming laptop",
            "limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["comparison"] is not None
    assert data["comparison"]["best_overall"] is not None
    assert data["comparison"]["cheapest"] is not None
    assert data["comparison"]["best_rated"] is not None
    assert data["comparison"]["best_deal"] is not None