from app.schemas.product import Product
from app.services.offer_grouping_service import (
    OfferGroupingService,
)


def make_product(
    title: str,
    price: float | None,
    source: str,
) -> Product:
    return Product(
        title=title,
        price=price,
        rating=4.5,
        review_count=1000,
        product_url=(
            f"https://example.com/{source.lower()}"
        ),
        source=source,
    )


def test_groups_same_product_from_different_sources():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
        make_product(
            "Samsung Galaxy A17 5g",
            29999,
            "Amazon",
        ),
    ]

    groups = service.group(products)

    assert len(groups) == 1

    grouped_products = next(
        iter(groups.values())
    )

    assert len(grouped_products) == 2


def test_keeps_different_products_separate():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
        make_product(
            "Samsung Galaxy A36 5G",
            28999,
            "Samsung",
        ),
    ]

    groups = service.group(products)

    assert len(groups) == 2


def test_best_offer_returns_cheapest_product():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            29999,
            "Amazon",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
    ]

    best = service.best_offer(products)

    assert best is not None
    assert best.price == 20499
    assert best.source == "Samsung"


def test_best_offer_ignores_products_without_price():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            None,
            "Amazon",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
    ]

    best = service.best_offer(products)

    assert best is not None
    assert best.price == 20499


def test_best_offer_returns_none_when_no_prices_exist():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            None,
            "Amazon",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            None,
            "Samsung",
        ),
    ]

    best = service.best_offer(products)

    assert best is None


def test_group_handles_empty_list():
    service = OfferGroupingService()

    groups = service.group([])

    assert groups == {}