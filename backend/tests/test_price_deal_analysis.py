from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.intelligence.deal_analysis import DealAnalysis


def test_analyzes_current_price_against_history():
    history = PriceHistory()

    history.add(60000, datetime(2026, 9, 1))
    history.add(55000, datetime(2026, 9, 2))
    history.add(52000, datetime(2026, 9, 3))

    analyzer = DealAnalysis()

    result = analyzer.analyze(
        current_price=52000,
        history=history,
    )

    assert result["lowest_price"] == 52000
    assert result["average_price"] == 55666.67
    assert result["deal_status"] == "Great Deal"


def test_detects_good_deal_from_history():
    history = PriceHistory()

    history.add(60000, datetime(2026, 9, 1))
    history.add(55000, datetime(2026, 9, 2))
    history.add(50000, datetime(2026, 9, 3))

    analyzer = DealAnalysis()

    result = analyzer.analyze(
        current_price=53000,
        history=history,
    )

    assert result["lowest_price"] == 50000
    assert result["average_price"] == 55000
    assert result["deal_status"] == "Good Deal"


def test_returns_unknown_without_price_history():
    history = PriceHistory()

    analyzer = DealAnalysis()

    result = analyzer.analyze(
        current_price=50000,
        history=history,
    )

    assert result["lowest_price"] is None
    assert result["average_price"] is None
    assert result["deal_status"] == "Unknown"