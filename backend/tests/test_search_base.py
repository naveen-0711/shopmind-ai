
import pytest

from app.ingestion.search_base import ProductSearchProvider


class TestProvider(ProductSearchProvider):

    def can_search(self, query: str) -> bool:
        return bool(query.strip())

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict]:

        return [
            {
                "title": "Test Laptop",
                "price": 70000,
                "rating": 4.5,
            }
        ]


def test_search_provider_is_abstract():
    with pytest.raises(TypeError):
        ProductSearchProvider()


def test_search_provider_can_search():
    provider = TestProvider()

    assert provider.can_search("gaming laptop") is True
    assert provider.can_search("") is False


@pytest.mark.anyio
async def test_search_provider_returns_products():
    provider = TestProvider()

    products = await provider.search(
        query="gaming laptop",
        max_price=80000,
        min_rating=4.0,
        limit=10,
    )

    assert len(products) == 1
    assert products[0]["title"] == "Test Laptop"
    assert products[0]["price"] == 70000
    assert products[0]["rating"] == 4.5

