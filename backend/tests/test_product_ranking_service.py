from app.schemas.product import Product
from app.services.product_ranking_service import ProductRankingService


def make_product(
    title: str,
    price: float | None = 20000,
    rating: float | None = 4.5,
    review_count: int | None = 100,
    deal_status: str = "Unknown",
) -> Product:
    return Product(
        title=title,
        price=price,
        currency="INR",
        rating=rating,
        review_count=review_count,
        product_url=f"https://example.com/{title.replace(' ', '-')}",
        source="Test",
        deal_status=deal_status,
    )


def test_higher_quality_product_should_rank_higher():
    service = ProductRankingService()

    strong = make_product(
        "Strong Product",
        price=20000,
        rating=4.8,
        review_count=5000,
    )
    weak = make_product(
        "Weak Product",
        price=20000,
        rating=4.1,
        review_count=50,
    )

    ranked = service.rank([weak, strong])

    assert ranked[0].title == "Strong Product"


def test_review_count_should_prevent_one_review_product_from_winning_automatically():
    service = ProductRankingService()

    popular = make_product(
        "Popular Product",
        price=20000,
        rating=4.8,
        review_count=8000,
    )
    suspicious = make_product(
        "Suspicious Product",
        price=18000,
        rating=5.0,
        review_count=1,
    )

    ranked = service.rank([suspicious, popular])

    assert ranked[0].title == "Popular Product"


def test_lower_price_should_help_when_quality_is_similar():
    service = ProductRankingService()

    expensive = make_product(
        "Expensive Product",
        price=30000,
        rating=4.7,
        review_count=2000,
    )
    cheaper = make_product(
        "Cheaper Product",
        price=25000,
        rating=4.7,
        review_count=2000,
    )

    ranked = service.rank([expensive, cheaper])

    assert ranked[0].title == "Cheaper Product"


def test_great_deal_should_boost_product():
    service = ProductRankingService()

    normal = make_product(
        "Normal Product",
        price=20000,
        rating=4.7,
        review_count=2000,
        deal_status="Normal",
    )
    great_deal = make_product(
        "Great Deal",
        price=20000,
        rating=4.6,
        review_count=1800,
        deal_status="Great Deal",
    )

    ranked = service.rank([normal, great_deal])

    assert ranked[0].title == "Great Deal"


def test_missing_rating_should_not_crash():
    service = ProductRankingService()

    product = make_product(
        "No Rating",
        price=20000,
        rating=None,
        review_count=100,
    )

    ranked = service.rank([product])

    assert len(ranked) == 1
    assert ranked[0].title == "No Rating"


def test_missing_review_count_should_not_crash():
    service = ProductRankingService()

    product = make_product(
        "No Reviews",
        price=20000,
        rating=4.5,
        review_count=None,
    )

    ranked = service.rank([product])

    assert len(ranked) == 1


def test_missing_price_should_not_crash():
    service = ProductRankingService()

    product = make_product(
        "No Price",
        price=None,
        rating=4.5,
        review_count=100,
    )

    ranked = service.rank([product])

    assert len(ranked) == 1


def test_rank_should_not_mutate_input():
    service = ProductRankingService()

    first = make_product("First", price=20000, rating=4.5, review_count=100)
    second = make_product("Second", price=15000, rating=4.6, review_count=200)

    products = [first, second]

    service.rank(products)

    assert products == [first, second]


def test_limit_should_be_respected():
    service = ProductRankingService()

    products = [
        make_product(f"Product {i}", price=20000 - i * 100)
        for i in range(10)
    ]

    ranked = service.rank(products, limit=3)

    assert len(ranked) == 3


def test_empty_products_returns_empty_list():
    service = ProductRankingService()

    assert service.rank([]) == []