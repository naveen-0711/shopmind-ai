
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


def test_ranking_returns_products_in_best_order():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=90000,
            rating=4.0,
            review_count=500,
        ),
        make_product(
            title="Product B",
            price=70000,
            rating=4.6,
            review_count=1500,
        ),
        make_product(
            title="Product C",
            price=80000,
            rating=4.3,
            review_count=1000,
        ),
    ]

    ranked = service.rank(products)

    assert len(ranked) == 3
    assert ranked[0].title == "Product B"
    assert ranked[1].title == "Product C"
    assert ranked[2].title == "Product A"


def test_ranking_does_not_modify_original_list():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=90000,
            rating=4.0,
            review_count=500,
        ),
        make_product(
            title="Product B",
            price=70000,
            rating=4.6,
            review_count=1500,
        ),
    ]

    original_order = [product.title for product in products]

    service.rank(products)

    assert [product.title for product in products] == original_order


def test_ranking_handles_missing_rating():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=70000,
            rating=4.5,
            review_count=1000,
        ),
        Product(
            title="Product B",
            price=60000,
            rating=None,
            review_count=None,
            product_url="https://example.com/product-b",
            source="test",
        ),
    ]

    ranked = service.rank(products)

    assert ranked[0].title == "Product A"


def test_ranking_handles_empty_list():
    service = ProductRankingService()

    ranked = service.rank([])

    assert ranked == []


def test_ranking_can_limit_results():
    service = ProductRankingService()

    products = [
        make_product(
            title="Product A",
            price=90000,
            rating=4.0,
            review_count=500,
        ),
        make_product(
            title="Product B",
            price=70000,
            rating=4.6,
            review_count=1500,
        ),
        make_product(
            title="Product C",
            price=80000,
            rating=4.3,
            review_count=1000,
        ),
    ]

    ranked = service.rank(
        products,
        limit=2,
    )

    assert len(ranked) == 2
    assert ranked[0].title == "Product B"
    assert ranked[1].title == "Product C"

