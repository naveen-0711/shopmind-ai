import pytest

from app.ingestion.providers.serpapi_search import (
    SerpApiSearchProvider,
)


# ============================================================
# Direct retailer URL extraction
# ============================================================


def test_extract_direct_retailer_url():
    provider = SerpApiSearchProvider(api_key="test-key")

    seller = {
        "name": "Amazon.in",
        "link": "https://www.google.com/url?q=https://amazon.in/product",
        "direct_link": "https://www.amazon.in/product",
    }

    result = provider._extract_direct_retailer_url(seller)

    assert result == "https://www.amazon.in/product"


def test_extract_direct_retailer_url_returns_none_when_missing():
    provider = SerpApiSearchProvider(api_key="test-key")

    seller = {
        "name": "Amazon.in",
        "link": "https://www.google.com/url?q=https://amazon.in/product",
    }

    result = provider._extract_direct_retailer_url(seller)

    assert result is None


def test_extract_direct_retailer_url_ignores_empty_value():
    provider = SerpApiSearchProvider(api_key="test-key")

    seller = {
        "name": "Amazon.in",
        "direct_link": "",
    }

    result = provider._extract_direct_retailer_url(seller)

    assert result is None


def test_extract_best_retailer_url_prefers_direct_link():
    provider = SerpApiSearchProvider(api_key="test-key")

    sellers = [
        {
            "name": "Amazon.in",
            "link": "https://www.google.com/url?q=https://amazon.in/product",
            "direct_link": "https://www.amazon.in/product",
        },
        {
            "name": "Flipkart",
            "link": "https://www.google.com/url?q=https://flipkart.com/product",
            "direct_link": "https://www.flipkart.com/product",
        },
    ]

    result = provider._extract_best_retailer_url(sellers)

    assert result == "https://www.amazon.in/product"


def test_extract_best_retailer_url_returns_none_when_no_direct_links():
    provider = SerpApiSearchProvider(api_key="test-key")

    sellers = [
        {
            "name": "Amazon.in",
            "link": "https://www.google.com/url?q=https://amazon.in/product",
        },
        {
            "name": "Flipkart",
            "link": "https://www.google.com/url?q=https://flipkart.com/product",
        },
    ]

    result = provider._extract_best_retailer_url(sellers)

    assert result is None


# ============================================================
# Immersive Product API retailer resolution
# ============================================================


@pytest.mark.asyncio
async def test_resolve_retailer_url_from_immersive_product_api(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request_immersive(
        self,
        page_token,
    ):
        assert page_token == "token123"

        return {
            "product_results": {
                "stores": [
                    {
                        "name": "Amazon.in",
                        "link": "https://www.amazon.in/product",
                    },
                    {
                        "name": "Flipkart",
                        "link": "https://www.flipkart.com/product",
                    },
                ]
            }
        }

    monkeypatch.setattr(
        provider,
        "_request_immersive_product",
        mock_request_immersive.__get__(provider),
    )

    result = await provider._resolve_retailer_url(
        page_token="token123",
        source="Amazon.in",
    )

    assert result == "https://www.amazon.in/product"


@pytest.mark.asyncio
async def test_resolve_retailer_url_matches_requested_source(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request_immersive(
        self,
        page_token,
    ):
        return {
            "product_results": {
                "stores": [
                    {
                        "name": "Flipkart",
                        "link": "https://www.flipkart.com/product",
                    },
                    {
                        "name": "Amazon.in",
                        "link": "https://www.amazon.in/product",
                    },
                ]
            }
        }

    monkeypatch.setattr(
        provider,
        "_request_immersive_product",
        mock_request_immersive.__get__(provider),
    )

    result = await provider._resolve_retailer_url(
        page_token="token123",
        source="Amazon.in",
    )

    assert result == "https://www.amazon.in/product"


@pytest.mark.asyncio
async def test_resolve_retailer_url_returns_none_when_no_stores(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request_immersive(
        self,
        page_token,
    ):
        return {
            "product_results": {
                "stores": []
            }
        }

    monkeypatch.setattr(
        provider,
        "_request_immersive_product",
        mock_request_immersive.__get__(provider),
    )

    result = await provider._resolve_retailer_url(
        page_token="token123",
        source="Amazon.in",
    )

    assert result is None


@pytest.mark.asyncio
async def test_resolve_retailer_url_returns_none_on_api_failure(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request_immersive(
        self,
        page_token,
    ):
        raise RuntimeError(
            "SerpApi request failed"
        )

    monkeypatch.setattr(
        provider,
        "_request_immersive_product",
        mock_request_immersive.__get__(provider),
    )

    result = await provider._resolve_retailer_url(
        page_token="token123",
        source="Amazon.in",
    )

    assert result is None


# ============================================================
# Search integration
# ============================================================


@pytest.mark.asyncio
async def test_search_result_uses_direct_retailer_url(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request(
        self,
        query,
        limit=10,
    ):
        return {
            "shopping_results": [
                {
                    "immersive_product_page_token": "token123",
                    "title": "Samsung Galaxy A36 5G",
                    "extracted_price": 28999,
                    "rating": 4.7,
                    "reviews": 17000,
                    "thumbnail": "https://example.com/image.jpg",
                    "product_link": (
                        "https://www.google.com/"
                        "shopping/product/abc123"
                    ),
                    "source": "Amazon.in",
                }
            ]
        }

    async def mock_resolve(
        page_token,
        source,
    ):
        assert page_token == "token123"
        assert source == "Amazon.in"

        return (
            "https://www.amazon.in/"
            "samsung-galaxy-a36"
        )

    monkeypatch.setattr(
        provider,
        "_request",
        mock_request.__get__(provider),
    )

    monkeypatch.setattr(
        provider,
        "_resolve_retailer_url",
        mock_resolve,
    )

    results = await provider.search(
        query="Samsung Galaxy A36",
        limit=10,
    )

    assert len(results) == 1

    assert results[0]["product_url"] == (
        "https://www.amazon.in/"
        "samsung-galaxy-a36"
    )


@pytest.mark.asyncio
async def test_search_result_falls_back_to_google_url_when_resolution_fails(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request(
        self,
        query,
        limit=10,
    ):
        return {
            "shopping_results": [
                {
                    "immersive_product_page_token": "token123",
                    "title": "Samsung Galaxy A36 5G",
                    "extracted_price": 28999,
                    "product_link": (
                        "https://www.google.com/"
                        "shopping/product/abc123"
                    ),
                    "source": "Amazon.in",
                }
            ]
        }

    async def mock_resolve(
        page_token,
        source,
    ):
        return None

    monkeypatch.setattr(
        provider,
        "_request",
        mock_request.__get__(provider),
    )

    monkeypatch.setattr(
        provider,
        "_resolve_retailer_url",
        mock_resolve,
    )

    results = await provider.search(
        query="Samsung Galaxy A36",
        limit=10,
    )

    assert len(results) == 1

    assert results[0]["product_url"] == (
        "https://www.google.com/"
        "shopping/product/abc123"
    )


@pytest.mark.asyncio
async def test_search_result_keeps_google_url_when_page_token_missing(
    monkeypatch,
):
    provider = SerpApiSearchProvider(api_key="test-key")

    async def mock_request(
        self,
        query,
        limit=10,
    ):
        return {
            "shopping_results": [
                {
                    "title": "Samsung Galaxy A36 5G",
                    "extracted_price": 28999,
                    "product_link": (
                        "https://www.google.com/"
                        "shopping/product/abc123"
                    ),
                    "source": "Amazon.in",
                }
            ]
        }

    async def mock_resolve(
        page_token,
        source,
    ):
        raise AssertionError(
            "Retailer resolution should not run "
            "without immersive_product_page_token"
        )

    monkeypatch.setattr(
        provider,
        "_request",
        mock_request.__get__(provider),
    )

    monkeypatch.setattr(
        provider,
        "_resolve_retailer_url",
        mock_resolve,
    )

    results = await provider.search(
        query="Samsung Galaxy A36",
        limit=10,
    )

    assert len(results) == 1

    assert results[0]["product_url"] == (
        "https://www.google.com/"
        "shopping/product/abc123"
    )