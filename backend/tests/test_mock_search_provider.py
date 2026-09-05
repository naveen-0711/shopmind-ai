
import pytest

from app.ingestion.providers.mock_search import MockSearchProvider


def test_mock_provider_can_search():
    provider = MockSearchProvider()

    assert provider.can_search("gaming laptop") is True
    assert provider.can_search("") is False


@pytest.mark.anyio
async def test_mock_provider_returns_products():
    provider = MockSearchProvider()

    results = await provider.search(
        query="gaming laptop",
        limit=5,
    )

    assert len(results) == 5

    assert results[0]["title"] == "Gaming Laptop Pro"
    assert results[0]["price"] == 74999
    assert results[0]["rating"] == 4.5
    assert results[0]["source"] == "mock"


@pytest.mark.anyio
async def test_mock_provider_respects_limit():
    provider = MockSearchProvider()

    results = await provider.search(
        query="laptop",
        limit=2,
    )

    assert len(results) == 2


@pytest.mark.anyio
async def test_mock_provider_supports_price_filter():
    provider = MockSearchProvider()

    results = await provider.search(
        query="laptop",
        max_price=80000,
        limit=10,
    )

    assert all(
        product["price"] <= 80000
        for product in results
    )

