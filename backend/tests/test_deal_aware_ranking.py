
from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.schemas.product import Product
from app.services.product_ranking_service import (
    ProductRankingService,
)


def make_product(
    title: str,
    price: float,
    rating: float,
    review_count: int,
) -> Product:
    return Product(
        title=title,
        price=price,
        rating=rating,
        review_count=review_count,
        product_url=f"https://example.com/{title.lower()}",
        source="test",
    )


def make_history(
    prices: list[float],
) -> PriceHistory:
    history = PriceHistory()

    for index, price in enumerate(prices):
        history.add(
            price=price,
            observed_at=datetime(2026, 1, index + 1),
        )

    return history


def test_great_deal_should_get_ranking_advantage():
    service = ProductRankingService()

    products = [
        make_product(
            title="Normal Price",
            price=70000,
            rating=4.6,
            review_count=1500,
        ),
        make_product(
            title="Historical Low",
            price=60000,
            rating=4.5,
            review_count=1400,
        ),
    ]

    histories = {
        "Normal Price": make_history(
            [68000, 69000, 70000, 71000]
        ),
        "Historical Low": make_history(
            [70000, 72000, 75000, 80000]
        ),
    }

    ranked = service.rank(
        products,
        histories=histories,
    )

    assert ranked[0].title == "Historical Low"
