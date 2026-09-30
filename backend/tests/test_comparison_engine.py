from app.intelligence.comparison_engine import ComparisonEngine
from app.schemas.search import ProductSearchProduct


def make_product(
    title: str,
    price: float,
    rating: float,
    review_count: int,
    recommendation_score: float,
    deal_status: str = "Unknown",
):
    return ProductSearchProduct(
        title=title,
        price=price,
        currency="INR",
        rating=rating,
        review_count=review_count,
        image_url=None,
        product_url=f"https://example.com/{title.lower().replace(' ', '-')}",
        source="test",
        lowest_price=None,
        average_price=None,
        deal_status=deal_status,
        offers=[],
        offer_count=1,
        savings=0,
        recommendation_score=recommendation_score,
        recommendation_reasons=[],
    )


def test_comparison_identifies_best_overall():
    products = [
        make_product(
            "Product A",
            50000,
            4.5,
            500,
            78,
        ),
        make_product(
            "Product B",
            55000,
            4.8,
            5000,
            91,
        ),
        make_product(
            "Product C",
            45000,
            4.2,
            300,
            70,
        ),
    ]

    result = ComparisonEngine().compare(products)

    assert result["best_overall"].title == "Product B"


def test_comparison_identifies_cheapest():
    products = [
        make_product("Product A", 50000, 4.5, 500, 78),
        make_product("Product B", 55000, 4.8, 5000, 91),
        make_product("Product C", 45000, 4.2, 300, 70),
    ]

    result = ComparisonEngine().compare(products)

    assert result["cheapest"].title == "Product C"


def test_comparison_identifies_best_rated():
    products = [
        make_product("Product A", 50000, 4.5, 500, 78),
        make_product("Product B", 55000, 4.8, 5000, 91),
        make_product("Product C", 45000, 4.2, 300, 70),
    ]

    result = ComparisonEngine().compare(products)

    assert result["best_rated"].title == "Product B"


def test_comparison_prefers_review_volume_when_ratings_are_close():
    products = [
        make_product("Low Review Product", 50000, 5.0, 12, 80),
        make_product("Trusted Product", 52000, 4.8, 8000, 82),
    ]

    result = ComparisonEngine().compare(products)

    assert result["best_overall"].title == "Trusted Product"


def test_comparison_identifies_best_deal():
    products = [
        make_product(
            "Normal Product",
            50000,
            4.5,
            1000,
            80,
            "Fair Price",
        ),
        make_product(
            "Good Deal Product",
            52000,
            4.5,
            1000,
            81,
            "Good Deal",
        ),
        make_product(
            "Great Deal Product",
            55000,
            4.4,
            1000,
            82,
            "Great Deal",
        ),
    ]

    result = ComparisonEngine().compare(products)

    assert result["best_deal"].title == "Great Deal Product"


def test_comparison_returns_empty_result_for_empty_products():
    result = ComparisonEngine().compare([])

    assert result["best_overall"] is None
    assert result["cheapest"] is None
    assert result["best_rated"] is None
    assert result["best_deal"] is None
    assert result["best_value"] is None