from typing import Any

from app.ingestion.search_base import ProductSearchProvider


class MockSearchProvider(ProductSearchProvider):
    """
    Fake marketplace search provider used for testing
    the search pipeline without external network requests.
    """

    def __init__(self) -> None:
        self.products = [
            {
                "title": "Gaming Laptop Pro",
                "price": 74999,
                "rating": 4.5,
                "review_count": 1200,
                "image_url": "https://example.com/laptop-pro.jpg",
                "product_url": "https://example.com/laptop-pro",
                "source": "mock",
                "currency": "INR",
            },
            {
                "title": "Gaming Laptop Air",
                "price": 64999,
                "rating": 4.2,
                "review_count": 850,
                "image_url": "https://example.com/laptop-air.jpg",
                "product_url": "https://example.com/laptop-air",
                "source": "mock",
                "currency": "INR",
            },
            {
                "title": "Budget Gaming Laptop",
                "price": 49999,
                "rating": 3.9,
                "review_count": 500,
                "image_url": "https://example.com/budget-laptop.jpg",
                "product_url": "https://example.com/budget-laptop",
                "source": "mock",
                "currency": "INR",
            },
            {
                "title": "Premium Gaming Laptop",
                "price": 99999,
                "rating": 4.8,
                "review_count": 2000,
                "image_url": "https://example.com/premium-laptop.jpg",
                "product_url": "https://example.com/premium-laptop",
                "source": "mock",
                "currency": "INR",
            },
            {
                "title": "Gaming Laptop Max",
                "price": 84999,
                "rating": 4.4,
                "review_count": 950,
                "image_url": "https://example.com/laptop-max.jpg",
                "product_url": "https://example.com/laptop-max",
                "source": "mock",
                "currency": "INR",
            },
            {
                "title": "Gaming Laptop Elite",
                "price": 67999,
                "rating": 4.7,
                "review_count": 1500,
                "image_url": "https://example.com/laptop-elite.jpg",
                "product_url": "https://example.com/laptop-elite",
                "source": "mock",
                "currency": "INR",
            },
        ]

    def can_search(self, query: str) -> bool:
        return bool(query.strip())

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:

        results = self.products

        if max_price is not None:
            results = [
                product
                for product in results
                if product["price"] <= max_price
            ]

        if min_rating is not None:
            results = [
                product
                for product in results
                if product["rating"] >= min_rating
            ]

        return results[:limit]
