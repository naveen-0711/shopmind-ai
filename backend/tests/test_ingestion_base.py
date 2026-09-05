import pytest

from app.ingestion.base import ProductAdapter


class TestAdapter(ProductAdapter):

    def can_handle(self, url: str) -> bool:
        return "example.com" in url

    async def fetch_product(self, url: str) -> dict:
        return {"url": url}


def test_adapter_can_handle():
    adapter = TestAdapter()

    assert adapter.can_handle("https://example.com/product") is True
    assert adapter.can_handle("https://google.com") is False


@pytest.mark.anyio
async def test_adapter_fetch_product():
    adapter = TestAdapter()

    result = await adapter.fetch_product("https://example.com/product")

    assert result["url"] == "https://example.com/product"