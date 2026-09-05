from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.product import Product
from app.services.product_service import ProductService


@pytest.mark.anyio
async def test_analyze_product():
    resolver = MagicMock()
    adapter = MagicMock()

    adapter.fetch_product = AsyncMock(
        return_value={
            "title": "Apple iPhone 15",
            "price": "69999",
            "rating": "4.5",
            "review_count": "1250",
            "image_url": "https://example.com/iphone.jpg",
        }
    )

    adapter.normalize_product = AsyncMock(
        return_value=Product(
            title="Apple iPhone 15",
            price=69999,
            currency="INR",
            rating=4.5,
            review_count=1250,
            image_url="https://example.com/iphone.jpg",
            product_url="https://www.amazon.in/dp/B0ABC123",
            source="amazon",
        )
    )

    resolver.resolve.return_value = adapter

    service = ProductService(resolver)

    result = await service.analyze_product(
        "https://www.amazon.in/dp/B0ABC123"
    )

    assert isinstance(result, Product)
    assert result.title == "Apple iPhone 15"
    assert result.price == 69999
    assert result.source == "amazon"

    resolver.resolve.assert_called_once_with(
        "https://www.amazon.in/dp/B0ABC123"
    )

    adapter.fetch_product.assert_awaited_once_with(
        "https://www.amazon.in/dp/B0ABC123"
    )

    adapter.normalize_product.assert_awaited_once()


@pytest.mark.anyio
async def test_unsupported_product_url():
    resolver = MagicMock()
    resolver.resolve.return_value = None

    service = ProductService(resolver)

    with pytest.raises(ValueError, match="Unsupported product URL"):
        await service.analyze_product(
            "https://www.example.com/product/123"
        )