from app.intelligence.product_intelligence import ProductIntelligenceService


def test_analyze_returns_quality_score():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert "quality_score" in result
    assert isinstance(result["quality_score"], (int, float))


def test_analyze_returns_discount_percentage():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert "discount_percentage" in result
    assert result["discount_percentage"] == 20


def test_analyze_returns_recommendation():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert "recommendation" in result
    assert isinstance(result["recommendation"], str)


def test_high_quality_product_gets_positive_recommendation():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert result["quality_score"] > 0
    assert result["discount_percentage"] == 20


def test_missing_rating_does_not_crash():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=None,
        review_count=100,
        current_price=20000,
        reference_price=25000,
    )

    assert "quality_score" in result


def test_missing_reviews_does_not_crash():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.5,
        review_count=None,
        current_price=20000,
        reference_price=25000,
    )

    assert "quality_score" in result


def test_missing_price_does_not_crash():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.5,
        review_count=100,
        current_price=None,
        reference_price=25000,
    )

    assert "discount_percentage" in result


def test_missing_reference_price_does_not_crash():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.5,
        review_count=100,
        current_price=20000,
        reference_price=None,
    )

    assert "discount_percentage" in result


def test_explain_returns_score_and_reasons():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
        deal_status="Great Deal",
    )

    assert "score" in result
    assert "reasons" in result

    assert isinstance(result["score"], float)
    assert isinstance(result["reasons"], list)

    assert len(result["reasons"]) > 0


def test_explain_high_rating_creates_rating_reason():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert any(
        "rating" in reason.lower()
        for reason in result["reasons"]
    )


def test_explain_high_review_count_creates_trust_reason():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert any(
        "review" in reason.lower()
        for reason in result["reasons"]
    )


def test_explain_great_deal_creates_deal_reason():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
        deal_status="Great Deal",
    )

    assert any(
        "deal" in reason.lower()
        for reason in result["reasons"]
    )


def test_explain_score_is_between_zero_and_hundred():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=4.8,
        review_count=8000,
        current_price=20000,
        reference_price=25000,
    )

    assert 0 <= result["score"] <= 100


def test_explain_missing_values_does_not_crash():
    service = ProductIntelligenceService()

    result = service.explain(
        rating=None,
        review_count=None,
        current_price=None,
        reference_price=None,
    )

    assert isinstance(result["score"], float)
    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) > 0