import pytest

from app.ingestion.providers.serpapi_search import (
    SerpApiSearchProvider,
)


def test_serpapi_provider_can_search_non_empty_query():
    provider = SerpApiSearchProvider(
        api_key="test-key"
    )

    assert provider.can_search("Samsung phone") is True


def test_serpapi_provider_rejects_empty_query():
    provider = SerpApiSearchProvider(
        api_key="test-key"
    )

    assert provider.can_search("") is False
    assert provider.can_search("   ") is False


@pytest.mark.anyio
async def test_serpapi_provider_maps_product_results(
    monkeypatch,
):
    provider = SerpApiSearchProvider(
        api_key="test-key"
    )

    async def fake_request(*args, **kwargs):
        return {
            "shopping_results": [
                {
                    "title": "Samsung Galaxy A56",
                    "link": "https://example.com/a56",
                    "price": "₹29,999",
                    "extracted_price": 29999,
                    "rating": 4.5,
                    "reviews": 1250,
                    "thumbnail": "https://example.com/a56.jpg",
                    "source": "Amazon.in",
                }
            ]
        }

    monkeypatch.setattr(
        provider,
        "_request",
        fake_request,
    )

    results = await provider.search(
        query="Samsung phone",
        max_price=30000,
        limit=10,
    )

    assert len(results) == 1

    product = results[0]

    assert product["title"] == "Samsung Galaxy A56"
    assert product["price"] == 29999
    assert product["rating"] == 4.5
    assert product["review_count"] == 1250
    assert product["product_url"] == (
        "https://example.com/a56"
    )
    assert product["image_url"] == (
        "https://example.com/a56.jpg"
    )
    assert product["source"] == "Amazon.in"
    assert product["currency"] == "INR"


@pytest.mark.anyio
async def test_serpapi_provider_respects_limit(
    monkeypatch,
):
    provider = SerpApiSearchProvider(
        api_key="test-key"
    )

    async def fake_request(*args, **kwargs):
        return {
            "shopping_results": [
                {
                    "title": "Product 1",
                    "link": "https://example.com/1",
                    "extracted_price": 10000,
                },
                {
                    "title": "Product 2",
                    "link": "https://example.com/2",
                    "extracted_price": 20000,
                },
                {
                    "title": "Product 3",
                    "link": "https://example.com/3",
                    "extracted_price": 30000,
                },
            ]
        }

    monkeypatch.setattr(
        provider,
        "_request",
        fake_request,
    )

    results = await provider.search(
        query="phones",
        limit=2,
    )

    assert len(results) == 2


@pytest.mark.anyio
async def test_serpapi_provider_excludes_products_without_rating_when_min_rating_is_set(
    monkeypatch,
):
    provider = SerpApiSearchProvider(
        api_key="test-key",
    )

    async def fake_request(*args, **kwargs):
        return {
            "shopping_results": [
                {
                    "title": "Highly Rated Phone",
                    "extracted_price": 25000,
                    "rating": 4.8,
                    "reviews": 1000,
                    "thumbnail": "https://example.com/high.jpg",
                    "product_link": "https://example.com/high",
                    "source": "Example Store",
                },
                {
                    "title": "Unrated Phone",
                    "extracted_price": 20000,
                    "rating": None,
                    "reviews": None,
                    "thumbnail": "https://example.com/unrated.jpg",
                    "product_link": "https://example.com/unrated",
                    "source": "Example Store",
                },
                {
                    "title": "Low Rated Phone",
                    "extracted_price": 18000,
                    "rating": 4.1,
                    "reviews": 500,
                    "thumbnail": "https://example.com/low.jpg",
                    "product_link": "https://example.com/low",
                    "source": "Example Store",
                },
            ]
        }

    monkeypatch.setattr(
        provider,
        "_request",
        fake_request,
    )

    results = await provider.search(
        query="Samsung phone",
        min_rating=4.5,
        limit=10,
    )

    assert len(results) == 1

    assert results[0]["title"] == "Highly Rated Phone"
    assert results[0]["rating"] == 4.8


def test_serpapi_provider_can_use_settings(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERPAPI_API_KEY",
        "configured-test-key",
    )

    from app.core.config import Settings

    settings = Settings()

    provider = SerpApiSearchProvider(
        api_key=settings.serpapi_api_key,
    )

    assert provider.api_key == "configured-test-key"


def test_search_uses_product_link(monkeypatch):
    provider = SerpApiSearchProvider(
        api_key="test-key",
    )

    async def fake_request(query, limit=10):
        return {
            "shopping_results": [
                {
                    "title": "Samsung Galaxy A06 5G",
                    "extracted_price": 15499,
                    "rating": 4.8,
                    "reviews": 1200,
                    "thumbnail": "https://example.com/image.jpg",
                    "product_link": (
                        "https://www.google.com/shopping/product/123"
                    ),
                    "source": "Samsung.com",
                }
            ]
        }

    monkeypatch.setattr(
        provider,
        "_request",
        fake_request,
    )

    import asyncio

    results = asyncio.run(
        provider.search(
            query="Samsung phone",
            limit=1,
        )
    )

    assert len(results) == 1

    assert (
        results[0]["product_url"]
        == "https://www.google.com/shopping/product/123"
    )


@pytest.mark.anyio
async def test_serpapi_provider_skips_invalid_product_data(
    monkeypatch,
):
    provider = SerpApiSearchProvider(
        api_key="test-key",
    )

    async def fake_request(*args, **kwargs):
        return {
            "shopping_results": [
                {
                    "title": "",
                    "extracted_price": 25000,
                    "rating": 4.8,
                    "reviews": 100,
                    "product_link": "https://example.com/invalid",
                    "source": "Example Store",
                },
                {
                    "title": "Valid Phone",
                    "extracted_price": 25000,
                    "rating": 4.8,
                    "reviews": 100,
                    "product_link": "https://example.com/valid",
                    "source": "Example Store",
                },
                {
                    "title": "Invalid Price Phone",
                    "extracted_price": 0,
                    "rating": 4.8,
                    "reviews": 100,
                    "product_link": "https://example.com/invalid-price",
                    "source": "Example Store",
                },
            ]
        }

    monkeypatch.setattr(
        provider,
        "_request",
        fake_request,
    )

    results = await provider.search(
        query="Samsung phone",
        limit=10,
    )

    assert len(results) == 1
    assert results[0]["title"] == "Valid Phone"
