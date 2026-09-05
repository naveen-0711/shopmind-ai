from unittest.mock import AsyncMock

import pytest

from app.ingestion.resolver import ProductResolver
from app.schemas.product import Product


@pytest.mark.anyio
async def test_product_ingestion_flow():
    resolver = ProductResolver()

    adapter = resolver.resolve(
        "https://www.amazon.in/dp/B0ABC123"
    )

    assert adapter is not None

    adapter.fetch_product = AsyncMock(
        return_value={
            "title": "Apple iPhone 15",
            "price": "69999",
            "rating": "4.5",
            "review_count": "1250",
            "image_url": "https://example.com/iphone.jpg",
        }
    )

    raw_data = await adapter.fetch_product(
        "https://www.amazon.in/dp/B0ABC123"
    )

    product = await adapter.normalize_product(
        raw_data,
        "https://www.amazon.in/dp/B0ABC123",
    )

    assert isinstance(product, Product)
    assert product.title == "Apple iPhone 15"
    assert product.price == 69999
    assert product.rating == 4.5
    assert product.review_count == 1250
    assert product.source == "amazon"


@pytest.mark.anyio
async def test_unsupported_product_url():
    resolver = ProductResolver()

    adapter = resolver.resolve(
        "https://www.example.com/product/123"
    )

    assert adapter is None