import pytest
from pydantic import ValidationError

from app.schemas.product import Product
from app.services.product_normalization_service import (
    ProductNormalizationService,
)


def test_normalization_converts_raw_result_to_product():
    service = ProductNormalizationService()

    raw_product = {
        "title": "Samsung Galaxy S24",
        "price": 69999,
        "rating": 4.5,
        "review_count": 1250,
        "image_url": "https://example.com/s24.jpg",
    }

    product = service.normalize(
        raw_product=raw_product,
        product_url="https://amazon.in/samsung-s24",
        source="amazon",
    )

    assert isinstance(product, Product)
    assert product.title == "Samsung Galaxy S24"
    assert product.price == 69999
    assert product.rating == 4.5
    assert product.review_count == 1250
    assert product.image_url == "https://example.com/s24.jpg"
    assert product.product_url == "https://amazon.in/samsung-s24"
    assert product.source == "amazon"
    assert product.currency == "INR"


def test_normalization_handles_missing_optional_fields():
    service = ProductNormalizationService()

    raw_product = {
        "title": "Budget Phone",
    }

    product = service.normalize(
        raw_product=raw_product,
        product_url="https://example.com/phone",
        source="example",
    )

    assert product.title == "Budget Phone"
    assert product.price is None
    assert product.rating is None
    assert product.review_count is None
    assert product.image_url is None
    assert product.currency == "INR"


def test_normalization_converts_numeric_values():
    service = ProductNormalizationService()

    raw_product = {
        "title": "Laptop",
        "price": "74999",
        "rating": "4.3",
        "review_count": "500",
    }

    product = service.normalize(
        raw_product=raw_product,
        product_url="https://example.com/laptop",
        source="example",
    )

    assert product.price == 74999.0
    assert product.rating == 4.3
    assert product.review_count == 500


def test_normalization_rejects_missing_title():
    service = ProductNormalizationService()

    raw_product = {
        "price": 50000,
        "rating": 4.5,
    }

    with pytest.raises((KeyError, ValidationError)):
        service.normalize(
            raw_product=raw_product,
            product_url="https://example.com/product",
            source="example",
        )


def test_normalization_preserves_source():
    service = ProductNormalizationService()

    raw_product = {
        "title": "Test Product",
        "price": 10000,
    }

    product = service.normalize(
        raw_product=raw_product,
        product_url="https://flipkart.com/test",
        source="flipkart",
    )

    assert product.source == "flipkart"
    assert product.product_url == "https://flipkart.com/test"

