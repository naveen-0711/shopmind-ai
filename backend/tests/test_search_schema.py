import pytest
from pydantic import ValidationError

from app.schemas.search import (
    ProductSearchRequest,
    ProductSearchResponse,
)


def test_search_request_accepts_valid_query():
    request = ProductSearchRequest(
        query="gaming laptop",
        max_price=80000,
        min_rating=4.0,
        limit=10,
    )

    assert request.query == "gaming laptop"
    assert request.max_price == 80000
    assert request.min_rating == 4.0
    assert request.limit == 10


def test_search_request_uses_default_values():
    request = ProductSearchRequest(
        query="iphone"
    )

    assert request.max_price is None
    assert request.min_rating is None
    assert request.limit == 10


def test_search_request_rejects_empty_query():
    with pytest.raises(ValidationError):
        ProductSearchRequest(query="")


def test_search_request_rejects_invalid_price():
    with pytest.raises(ValidationError):
        ProductSearchRequest(
            query="laptop",
            max_price=0,
        )


def test_search_request_rejects_invalid_rating():
    with pytest.raises(ValidationError):
        ProductSearchRequest(
            query="laptop",
            min_rating=6,
        )


def test_search_request_rejects_invalid_limit():
    with pytest.raises(ValidationError):
        ProductSearchRequest(
            query="laptop",
            limit=0,
        )


def test_search_response_contains_products():
    response = ProductSearchResponse(
        query="gaming laptop",
        products=[
            {
                "title": "Example Laptop",
                "price": 70000,
            }
        ],
        total=1,
    )

    assert response.query == "gaming laptop"
    assert response.total == 1
    assert len(response.products) == 1