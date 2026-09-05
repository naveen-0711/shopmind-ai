
import pytest

from app.ingestion.search_base import ProductSearchProvider


class FailingSearchProvider(ProductSearchProvider):
    def can_search(self, query: str) -> bool:
        return True

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict]:
        raise RuntimeError("Search provider unavailable")


def test_search_provider_is_abstract():
    with pytest.raises(TypeError):
        ProductSearchProvider()


@pytest.mark.anyio
async def test_provider_can_raise_runtime_error():
    provider = FailingSearchProvider()

    with pytest.raises(RuntimeError, match="Search provider unavailable"):
        await provider.search(
            query="Samsung phone"
        )
