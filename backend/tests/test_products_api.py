from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from app.api.routes.products import get_product_service
from app.main import app
from app.schemas.product import Product


client = TestClient(app)


def test_analyze_product_api():
    expected_product = Product(
        title="Apple iPhone 15",
        price=69999,
        currency="INR",
        rating=4.5,
        review_count=1250,
        image_url="https://example.com/iphone.jpg",
        product_url="https://www.amazon.in/dp/B0ABC123",
        source="amazon",
    )

    mock_service = MagicMock()
    mock_service.analyze_product = AsyncMock(
        return_value=expected_product
    )

    app.dependency_overrides[get_product_service] = (
        lambda: mock_service
    )

    try:
        response = client.post(
            "/api/v1/products/analyze",
            json={
                "url": "https://www.amazon.in/dp/B0ABC123"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["title"] == "Apple iPhone 15"
        assert data["price"] == 69999
        assert data["currency"] == "INR"
        assert data["rating"] == 4.5
        assert data["review_count"] == 1250
        assert data["source"] == "amazon"

        mock_service.analyze_product.assert_awaited_once_with(
            "https://www.amazon.in/dp/B0ABC123"
        )

    finally:
        app.dependency_overrides.clear()


def test_analyze_product_invalid_url():
    response = client.post(
        "/api/v1/products/analyze",
        json={
            "url": "not-a-valid-url"
        },
    )

    assert response.status_code == 422

def test_analyze_product_unsupported_url():
    from app.api.routes.products import get_product_service

    mock_service = MagicMock()
    mock_service.analyze_product = AsyncMock(
        side_effect=ValueError("Unsupported product URL")
    )

    app.dependency_overrides[get_product_service] = (
        lambda: mock_service
    )

    try:
        response = client.post(
            "/api/v1/products/analyze",
            json={
                "url": "https://www.example.com/product/123"
            },
        )

        assert response.status_code == 400

        data = response.json()

        assert data["detail"] == "Unsupported product URL"

    finally:
        app.dependency_overrides.clear()

def test_analyze_product_extraction_failure():
    from app.api.routes.products import get_product_service

    mock_service = MagicMock()
    mock_service.analyze_product = AsyncMock(
        side_effect=RuntimeError("Amazon extraction failed")
    )

    app.dependency_overrides[get_product_service] = (
        lambda: mock_service
    )

    try:
        response = client.post(
            "/api/v1/products/analyze",
            json={
                "url": "https://www.amazon.in/dp/B0ABC123"
            },
        )

        assert response.status_code == 502

        data = response.json()

        assert data["detail"] == "Product extraction failed"

    finally:
        app.dependency_overrides.clear()