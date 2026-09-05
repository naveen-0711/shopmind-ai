
from app.schemas.product import Product
from app.services.product_ranking_service import (
    ProductRankingService,
)


def make_product(
    title: str,
    price: float | None,
    rating: float | None,
    review_count: int | None,
) -> Product:
    return Product(
        title=title,
        price=price,
        rating=rating,
        review_count=review_count,
        product_url=f"https://example.com/{title.lower()}",
        source="test",
    )


def test_quality_rating_should_be_a_strong_ranking_signal():
    service = ProductRankingService()

    products = [
        make_product(
            title="Low Rated",
            price=50000,
            rating=3.5,
            review_count=1000,
        ),
        make_product(
            title="Highly Rated",
            price=50000,
            rating=4.8,
            review_count=1000,
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Highly Rated"


def test_lower_price_should_help_when_quality_is_similar():
    service = ProductRankingService()

    products = [
        make_product(
            title="Expensive",
            price=90000,
            rating=4.5,
            review_count=1000,
        ),
        make_product(
            title="Affordable",
            price=60000,
            rating=4.5,
            review_count=1000,
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Affordable"


def test_reviews_should_help_distinguish_products_with_same_rating():
    service = ProductRankingService()

    products = [
        make_product(
            title="Few Reviews",
            price=70000,
            rating=4.5,
            review_count=50,
        ),
        make_product(
            title="Many Reviews",
            price=70000,
            rating=4.5,
            review_count=5000,
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Many Reviews"


def test_missing_product_data_should_not_crash_ranking():
    service = ProductRankingService()

    products = [
        make_product(
            title="Complete",
            price=70000,
            rating=4.5,
            review_count=1000,
        ),
        make_product(
            title="Incomplete",
            price=None,
            rating=None,
            review_count=None,
        ),
    ]

    ranked = service.rank(products)

    assert len(ranked) == 2
    assert ranked[0].title == "Complete"


def test_ranking_should_be_deterministic():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=70000,
            rating=4.5,
            review_count=1000,
        ),
        make_product(
            title="Product B",
            price=70000,
            rating=4.5,
            review_count=1000,
        ),
    ]

    first_result = service.rank(products)
    second_result = service.rank(products)

    assert [p.title for p in first_result] == [
        p.title for p in second_result
    ]


def test_better_value_product_should_rank_higher():
    service = ProductRankingService()

    products = [
        make_product(
            title="Premium Expensive",
            price=100000,
            rating=4.7,
            review_count=2000,
        ),
        make_product(
            title="Excellent Value",
            price=60000,
            rating=4.6,
            review_count=1800,
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Excellent Value"


def test_price_advantage_should_be_relative_to_compared_products():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=80000,
            rating=4.5,
            review_count=1000,
        ),
        make_product(
            title="Product B",
            price=60000,
            rating=4.5,
            review_count=1000,
        ),
        make_product(
            title="Product C",
            price=40000,
            rating=4.5,
            review_count=1000,
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Product C"
    assert ranked[1].title == "Product B"
    assert ranked[2].title == "Product A"


