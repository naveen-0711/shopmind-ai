from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.schemas.product import Product
from app.services.product_ranking_service import (
    ProductRankingService,
)


class FakePriceHistoryService:
    def __init__(self, histories):
        self.histories = histories

    def get_history(self, product_id: int) -> PriceHistory:
        return self.histories[product_id]


def make_product(
    title: str,
    price: float,
) -> Product:
    return Product(
        title=title,
        price=price,
        rating=4.5,
        review_count=1000,
        product_url=f"https://example.com/{title.lower()}",
        source="test",
    )


def make_history(prices: list[float]) -> PriceHistory:
    history = PriceHistory()

    for index, price in enumerate(prices):
        history.add(
            price=price,
            observed_at=datetime(2026, 1, index + 1),
        )

    return history


def test_ranking_can_use_persistent_price_history():
    products = [
        make_product(
            title="Product A",
            price=70000,
        ),
        make_product(
            title="Product B",
            price=60000,
        ),
    ]

    histories = {
        1: make_history(
            [65000, 68000, 70000]
        ),
        2: make_history(
            [70000, 75000, 80000]
        ),
    }

    history_service = FakePriceHistoryService(
        histories
    )

    ranking_service = ProductRankingService()

    product_histories = {
        product.title: history_service.get_history(
            product_id=index
        )
        for index, product in enumerate(
            products,
            start=1,
        )
    }

    ranked = ranking_service.rank(
        products,
        histories=product_histories,
    )

    assert ranked[0].title == "Product B"
