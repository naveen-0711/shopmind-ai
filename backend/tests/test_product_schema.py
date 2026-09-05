import pytest
from pydantic import ValidationError

from app.schemas.product import ProductAnalyzeRequest


def test_valid_url():
    request = ProductAnalyzeRequest(
        url="https://www.amazon.in/dp/B09XS7JWHH"
    )

    assert str(request.url) == "https://www.amazon.in/dp/B09XS7JWHH"


def test_invalid_url():
    with pytest.raises(ValidationError):
        ProductAnalyzeRequest(
            url="not-a-valid-url"
        )






from app.schemas.product import Product

def test_product_schema():
    product = Product(
        title="Apple iPhone 15",
        price=69999,
        currency="INR",
        rating=4.5,
        review_count=1250,
        image_url="https://example.com/iphone.jpg",
        product_url="https://www.amazon.in/dp/example",
        source="amazon",
    )

    assert product.title == "Apple iPhone 15"
    assert product.price == 69999
    assert product.currency == "INR"
    assert product.rating == 4.5
    assert product.review_count == 1250
    assert product.source == "amazon"


def test_product_optional_fields():
    product = Product(
        title="Test Product",
        product_url="https://example.com/product",
        source="example",
    )

    assert product.price is None
    assert product.rating is None
    assert product.review_count is None
    assert product.image_url is None