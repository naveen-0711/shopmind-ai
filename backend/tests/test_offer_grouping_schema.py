from app.schemas.offer import (
    GroupedProduct,
    ProductOffer,
)
from app.schemas.product import Product
from app.services.offer_grouping_service import (
    OfferGroupingService,
)


def make_product(
    title: str,
    price: float,
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


def test_create_grouped_product_preserves_all_offers():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            29999,
            "Amazon",
        ),
    ]

    grouped = service.create_grouped_product(
        products
    )

    assert grouped is not None

    assert grouped.title == (
        "Samsung Galaxy A17 5G"
    )

    assert grouped.price == 20499

    assert grouped.offer_count == 2

    assert len(grouped.offers) == 2


def test_create_grouped_product_selects_cheapest_offer():
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

    grouped = service.create_grouped_product(
        products
    )

    assert grouped is not None

    assert grouped.price == 20499


def test_create_grouped_product_calculates_savings():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            29999,
            "Amazon",
        ),
    ]

    grouped = service.create_grouped_product(
        products
    )

    assert grouped is not None

    assert grouped.savings == 9500


def test_group_products_returns_one_product_per_identity():
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
        make_product(
            "Samsung Galaxy A36 5G",
            28999,
            "Samsung",
        ),
    ]

    grouped = service.group_products(
        products
    )

    assert len(grouped) == 2

    titles = {
        product.title
        for product in grouped
    }

    assert "Samsung Galaxy A17 5G" in titles
    assert "Samsung Galaxy A36 5G" in titles


def test_grouped_product_contains_offer_details():
    service = OfferGroupingService()

    products = [
        make_product(
            "Samsung Galaxy A17 5G",
            20499,
            "Samsung",
        ),
        make_product(
            "Samsung Galaxy A17 5G",
            29999,
            "Amazon",
        ),
    ]

    grouped = service.create_grouped_product(
        products
    )

    assert grouped is not None

    assert isinstance(
        grouped.offers[0],
        ProductOffer,
    )

    assert all(
        offer.product_url
        for offer in grouped.offers
    )


def test_grouped_product_schema_is_valid():
    grouped = GroupedProduct(
        title="Samsung Galaxy A17 5G",
        price=20499,
        product_url="https://example.com/samsung-a17",
        source="Samsung.com",
        offers=[],
    )

    assert grouped.title == (
        "Samsung Galaxy A17 5G"
    )

    assert grouped.offer_count == 0
    assert grouped.product_url == "https://example.com/samsung-a17"
    assert grouped.source == "Samsung.com"