from app.intelligence.product_intelligence import (
    ProductIntelligenceService,
)


def test_product_intelligence_combines_all_signals():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=5000,
        current_price=48000,
        reference_price=60000,
    )

    assert result["quality_score"] == 96.8
    assert result["discount_percentage"] == 20.0
    assert result["recommendation"] == "Strong Buy"


def test_product_intelligence_handles_missing_price():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=4.8,
        review_count=5000,
        current_price=None,
        reference_price=None,
    )

    assert result["quality_score"] == 96.8
    assert result["discount_percentage"] == 0.0
    assert result["recommendation"] == "Good Buy"


def test_product_intelligence_handles_low_quality_product():
    service = ProductIntelligenceService()

    result = service.analyze(
        rating=2.0,
        review_count=50,
        current_price=9000,
        reference_price=10000,
    )

    assert result["quality_score"] == 33.0
    assert result["discount_percentage"] == 10.0
    assert result["recommendation"] == "Poor Value"