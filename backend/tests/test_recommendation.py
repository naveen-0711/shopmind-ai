from app.intelligence.recommendation import RecommendationEngine


def test_high_quality_and_good_discount_is_strong_buy():
    engine = RecommendationEngine()

    result = engine.evaluate(
        quality_score=95,
        discount=20,
    )

    assert result == "Strong Buy"


def test_good_quality_is_good_buy():
    engine = RecommendationEngine()

    result = engine.evaluate(
        quality_score=85,
        discount=5,
    )

    assert result == "Good Buy"


def test_average_product_should_be_considered():
    engine = RecommendationEngine()

    result = engine.evaluate(
        quality_score=65,
        discount=5,
    )

    assert result == "Consider"


def test_low_quality_product_is_poor_value():
    engine = RecommendationEngine()

    result = engine.evaluate(
        quality_score=35,
        discount=10,
    )

    assert result == "Poor Value"


def test_high_quality_with_no_discount_is_still_good_buy():
    engine = RecommendationEngine()

    result = engine.evaluate(
        quality_score=90,
        discount=0,
    )

    assert result == "Good Buy"