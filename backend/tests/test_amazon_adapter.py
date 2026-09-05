import pytest

from app.ingestion.adapters.amazon import AmazonAdapter
from app.schemas.product import Product


def test_amazon_adapter_can_handle_amazon_url():
    adapter = AmazonAdapter()

    assert adapter.can_handle(
        "https://www.amazon.in/dp/B0ABC123"
    ) is True


def test_amazon_adapter_cannot_handle_other_url():
    adapter = AmazonAdapter()

    assert adapter.can_handle(
        "https://www.flipkart.com/product/123"
    ) is False


@pytest.mark.anyio
async def test_amazon_adapter_normalizes_product():
    adapter = AmazonAdapter()

    raw_data = {
        "title": "Apple iPhone 15",
        "price": "69999",
        "rating": "4.5",
        "review_count": "1250",
        "image_url": "https://example.com/iphone.jpg",
    }

    product = await adapter.normalize_product(
        raw_data,
        "https://www.amazon.in/dp/B0ABC123",
    )

    assert isinstance(product, Product)

    assert product.title == "Apple iPhone 15"
    assert product.price == 69999
    assert product.currency == "INR"
    assert product.rating == 4.5
    assert product.review_count == 1250
    assert product.image_url == "https://example.com/iphone.jpg"
    assert product.product_url == "https://www.amazon.in/dp/B0ABC123"
    assert product.source == "amazon"


@pytest.mark.anyio
async def test_amazon_adapter_handles_missing_optional_data():
    adapter = AmazonAdapter()

    raw_data = {
        "title": "Test Product",
    }

    product = await adapter.normalize_product(
        raw_data,
        "https://www.amazon.in/dp/B0ABC123",
    )

    assert product.title == "Test Product"
    assert product.price is None
    assert product.rating is None
    assert product.review_count is None
    assert product.image_url is None