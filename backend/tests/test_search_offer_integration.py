import pytest

from app.ingestion.search_base import ProductSearchProvider
from app.schemas.product import Product
from app.services.offer_grouping_service import OfferGroupingService
from app.services.product_search_service import ProductSearchService


class FakeSearchProvider(ProductSearchProvider):
    def can_search(self, query: str) -> bool:
        return True

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict]:
        return [
            {
                "title": "Samsung Galaxy A17 5G",
                "price": 20499,
                "rating": 4.5,
                "review_count": 16000,
                "product_url": "https://samsung.com/a17",
                "source": "Samsung.com",
                "currency": "INR",
            },
            {
                "title": "Samsung Galaxy A17 5G",
                "price": 29999,
                "rating": 5.0,
                "review_count": 13,
                "product_url": "https://amazon.in/a17",
                "source": "Amazon.in",
                "currency": "INR",
            },
        ]


@pytest.mark.asyncio
async def test_search_groups_same_product_into_multiple_offers():
    service = ProductSearchService(
        providers=[FakeSearchProvider()]
    )

    products = await service.search(
        query="Samsung Galaxy A17 5G",
        limit=10,
    )

    grouping_service = OfferGroupingService()
    grouped_products = grouping_service.group_products(products)

    assert len(grouped_products) == 1

    product = grouped_products[0]

    assert product.title == "Samsung Galaxy A17 5G"
    assert product.price == 20499
    assert product.offer_count == 2
    assert len(product.offers) == 2

    assert product.offers[0].source == "Samsung.com"
    assert product.offers[1].source == "Amazon.in"

    assert product.savings == 9500