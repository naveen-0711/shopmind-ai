from app.intelligence.product_scoring import ProductScorer


def test_high_rated_product_gets_high_score():
    scorer = ProductScorer()

    score = scorer.calculate(
        rating=4.8,
        review_count=5000,
    )

    assert score >= 90


def test_medium_rated_product_gets_medium_score():
    scorer = ProductScorer()

    score = scorer.calculate(
        rating=3.5,
        review_count=500,
    )

    assert 50 <= score < 90


def test_low_rated_product_gets_low_score():
    scorer = ProductScorer()

    score = scorer.calculate(
        rating=2.0,
        review_count=50,
    )

    assert score < 50


def test_missing_rating_returns_zero():
    scorer = ProductScorer()

    score = scorer.calculate(
        rating=None,
        review_count=500,
    )

    assert score == 0


def test_score_is_between_zero_and_hundred():
    scorer = ProductScorer()

    score = scorer.calculate(
        rating=5.0,
        review_count=100000,
    )

    assert 0 <= score <= 100