from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.intelligence.product_intelligence import ProductIntelligenceService


def test_complete_product_analysis():
    history = PriceHistory()

    history.add(60000, datetime(2026, 9, 1))
    history.add(55000, datetime(2026, 9, 2))
    history.add(52000, datetime(2026, 9, 3))

    service = ProductIntelligenceService()

    result = service.analyze_complete(
        rating=4.5,
        review_count=1000,
        current_price=52000,
        reference_price=60000,
        history=history,
    )

    assert result["quality_score"] == 92.0
    assert result["discount_percentage"] == 13.33
    assert result["lowest_price"] == 52000
    assert result["average_price"] == 55666.67
    assert result["deal_status"] == "Great Deal"
    assert result["recommendation"] == "Good Buy"


def test_complete_analysis_with_missing_history():
    history = PriceHistory()

    service = ProductIntelligenceService()

    result = service.analyze_complete(
        rating=4.0,
        review_count=500,
        current_price=50000,
        reference_price=60000,
        history=history,
    )

    assert result["quality_score"] == 74.0
    assert result["discount_percentage"] == 16.67
    assert result["lowest_price"] is None
    assert result["average_price"] is None
    assert result["deal_status"] == "Unknown"
    assert result["recommendation"] == "Consider"
