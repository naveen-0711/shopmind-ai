
import pytest
import asyncio

from app.ingestion.search_base import ProductSearchProvider
from app.schemas.product import Product
from app.services.product_search_service import ProductSearchService


class FakeSearchProvider:
    def __init__(self, products, can_search=True):
        self.products = products
        self._can_search = can_search

    def can_search(self, query: str) -> bool:
        return self._can_search

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict]:

        results = []

        for index, product in enumerate(self.products):
            results.append(
                {
                    **product,
                    "product_url": product.get(
                        "product_url",
                        f"https://example.com/product-{index}",
                    ),
                    "source": product.get(
                        "source",
                        "fake",
                    ),
                }
            )

        return results[:limit]


@pytest.mark.anyio
async def test_search_service_combines_provider_results():
    provider_one = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            }
        ]
    )

    provider_two = FakeSearchProvider(
        [
            {
                "title": "Laptop B",
                "price": 75000,
                "rating": 4.2,
            }
        ]
    )

    service = ProductSearchService(
        providers=[
            provider_one,
            provider_two,
        ]
    )

    results = await service.search(
        query="gaming laptop"
    )

    assert len(results) == 2

    assert isinstance(results[0], Product)
    assert isinstance(results[1], Product)

    assert results[0].title == "Laptop A"
    assert results[1].title == "Laptop B"


@pytest.mark.anyio
async def test_search_service_ignores_provider_that_cannot_search():
    usable_provider = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            }
        ]
    )

    unusable_provider = FakeSearchProvider(
        [
            {
                "title": "Laptop B",
                "price": 75000,
                "rating": 4.2,
            }
        ],
        can_search=False,
    )

    service = ProductSearchService(
        providers=[
            usable_provider,
            unusable_provider,
        ]
    )

    results = await service.search(
        query="gaming laptop"
    )

    assert len(results) == 1
    assert isinstance(results[0], Product)
    assert results[0].title == "Laptop A"


@pytest.mark.anyio
async def test_search_service_filters_by_max_price():
    provider = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            },
            {
                "title": "Laptop B",
                "price": 90000,
                "rating": 4.7,
            },
        ]
    )

    service = ProductSearchService(
        providers=[provider]
    )

    results = await service.search(
        query="gaming laptop",
        max_price=80000,
    )

    assert len(results) == 1
    assert isinstance(results[0], Product)
    assert results[0].title == "Laptop A"
    assert results[0].price == 70000


@pytest.mark.anyio
async def test_search_service_filters_by_min_rating():
    provider = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            },
            {
                "title": "Laptop B",
                "price": 75000,
                "rating": 3.8,
            },
        ]
    )

    service = ProductSearchService(
        providers=[provider]
    )

    results = await service.search(
        query="gaming laptop",
        min_rating=4.0,
    )

    assert len(results) == 1
    assert isinstance(results[0], Product)
    assert results[0].title == "Laptop A"
    assert results[0].rating == 4.5


@pytest.mark.anyio
async def test_search_service_respects_limit():
    provider = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            },
            {
                "title": "Laptop B",
                "price": 75000,
                "rating": 4.2,
            },
            {
                "title": "Laptop C",
                "price": 78000,
                "rating": 4.1,
            },
        ]
    )

    service = ProductSearchService(
        providers=[provider]
    )

    results = await service.search(
        query="gaming laptop",
        limit=2,
    )

    assert len(results) == 2
    assert all(
        isinstance(product, Product)
        for product in results
    )


@pytest.mark.anyio
async def test_search_service_returns_normalized_products():
    provider = FakeSearchProvider(
        [
            {
                "title": "Samsung Galaxy S24",
                "price": "69999",
                "rating": "4.5",
                "review_count": "1250",
                "image_url": "https://example.com/s24.jpg",
                "product_url": "https://amazon.in/s24",
                "source": "amazon",
            }
        ]
    )

    service = ProductSearchService(
        providers=[provider]
    )

    results = await service.search(
        query="Samsung Galaxy S24"
    )

    assert len(results) == 1

    product = results[0]

    assert isinstance(product, Product)
    assert product.title == "Samsung Galaxy S24"
    assert product.price == 69999.0
    assert product.rating == 4.5
    assert product.review_count == 1250
    assert product.image_url == "https://example.com/s24.jpg"
    assert product.product_url == "https://amazon.in/s24"
    assert product.source == "amazon"
    assert product.currency == "INR"


class FakeRankingService:
    def __init__(self):
        self.called = False
        self.received_products = None
        self.received_histories = None
        self.received_limit = None

    def rank(
        self,
        products,
        limit=None,
        histories=None,
    ):
        self.called = True
        self.received_products = products
        self.received_histories = histories
        self.received_limit = limit

        return list(reversed(products))[:limit]


@pytest.mark.anyio
async def test_search_service_uses_ranking_service():
    provider = FakeSearchProvider(
        [
            {
                "title": "Laptop A",
                "price": 70000,
                "rating": 4.5,
            },
            {
                "title": "Laptop B",
                "price": 75000,
                "rating": 4.2,
            },
        ]
    )

    ranking_service = FakeRankingService()

    service = ProductSearchService(
        providers=[provider],
        ranking_service=ranking_service,
    )

    results = await service.search(
        query="gaming laptop",
        limit=2,
    )

    assert ranking_service.called is True
    assert len(ranking_service.received_products) == 2
    assert ranking_service.received_limit == 2

    assert results[0].title == "Laptop B"
    assert results[1].title == "Laptop A"


def test_search_service_parses_natural_language_query():
    from app.ingestion.providers.mock_search import MockSearchProvider
    from app.services.product_search_service import ProductSearchService

    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    import asyncio

    results = asyncio.run(
        service.search(
            query="gaming laptop under 70000"
        )
    )

    assert all(
        product.price is None
        or product.price <= 70000
        for product in results
    )


def test_search_service_parses_natural_language_rating():
    from app.ingestion.providers.mock_search import MockSearchProvider
    from app.services.product_search_service import ProductSearchService

    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    import asyncio

    results = asyncio.run(
        service.search(
            query="gaming laptop with rating 4.5+"
        )
    )

    assert all(
        product.rating is None
        or product.rating >= 4.5
        for product in results
    )



import asyncio

from app.ingestion.providers.mock_search import MockSearchProvider
from app.services.product_search_service import ProductSearchService


def test_search_service_passes_parsed_constraints_to_provider():
    provider = MockSearchProvider()

    original_search = provider.search

    captured = {}

    async def tracked_search(
        query,
        max_price=None,
        min_rating=None,
        limit=10,
    ):
        captured["query"] = query
        captured["max_price"] = max_price
        captured["min_rating"] = min_rating
        captured["limit"] = limit

        return await original_search(
            query=query,
            max_price=max_price,
            min_rating=min_rating,
            limit=limit,
        )

    provider.search = tracked_search

    service = ProductSearchService(
        providers=[provider]
    )

    asyncio.run(
        service.search(
            query="best gaming laptop under 70000 "
                  "with rating 4.5+",
            limit=5,
        )
    )

    assert captured["query"] == "gaming laptop"
    assert captured["max_price"] == 70000
    assert captured["min_rating"] == 4.5
    assert captured["limit"] == 5


def test_search_service_excludes_products_without_rating_when_min_rating_is_set():
    from app.ingestion.providers.mock_search import MockSearchProvider
    from app.services.product_search_service import ProductSearchService

    service = ProductSearchService(
        providers=[MockSearchProvider()]
    )

    import asyncio

    results = asyncio.run(
        service.search(
            query="gaming laptop with rating 4.5+"
        )
    )

    assert all(
        product.rating is not None
        and product.rating >= 4.5
        for product in results
    )


@pytest.mark.asyncio
async def test_search_service_excludes_products_without_rating_when_min_rating_is_set():
    provider = MockSearchProvider()

    service = ProductSearchService(
        providers=[provider],
    )

    results = await service.search(
        query="gaming laptop",
        min_rating=4.5,
    )

    assert results

    for product in results:
        assert product.rating is not None
        assert product.rating >= 4.5

@pytest.mark.anyio
async def test_search_service_persists_products():
    from app.ingestion.providers.mock_search import MockSearchProvider
    from app.services.product_search_service import ProductSearchService

    class FakePersistenceService:
        def __init__(self):
            self.saved_products = []

        def save_product(
            self,
            title,
            product_url,
            source,
            currency="INR",
            rating=None,
            review_count=None,
            image_url=None,
            current_price=None,
            observed_at=None,
        ):
            self.saved_products.append(
                {
                    "title": title,
                    "product_url": product_url,
                    "source": source,
                    "currency": currency,
                    "rating": rating,
                    "review_count": review_count,
                    "image_url": image_url,
                    "current_price": current_price,
                }
            )

    persistence_service = FakePersistenceService()

    service = ProductSearchService(
        providers=[MockSearchProvider()],
        persistence_service=persistence_service,
    )

    results = await service.search(
        query="gaming laptop",
        limit=2,
    )

    assert len(results) == 2
    assert len(persistence_service.saved_products) == 2

    assert (
        persistence_service.saved_products[0]["title"]
        == results[0].title
    )

    assert (
        persistence_service.saved_products[0]["current_price"]
        == results[0].price
    )

class DuplicateSearchProvider(ProductSearchProvider):
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
                "title": "Samsung Galaxy A56",
                "price": 29999,
                "rating": 4.5,
                "review_count": 1200,
                "image_url": "https://example.com/a56.jpg",
                "product_url": "https://example.com/a56",
                "source": "Amazon",
                "currency": "INR",
            },
            {
                "title": "Samsung Galaxy A56",
                "price": 28999,
                "rating": 4.5,
                "review_count": 1200,
                "image_url": "https://example.com/a56.jpg",
                "product_url": "https://example.com/a56",
                "source": "Flipkart",
                "currency": "INR",
            },
        ]


def test_product_search_removes_duplicate_products():
    service = ProductSearchService(
        providers=[DuplicateSearchProvider()]
    )

    products = asyncio.run(
        service.search(
            query="Samsung phone",
            limit=10,
        )
    )

    assert len(products) == 1
    assert products[0].title == "Samsung Galaxy A56"