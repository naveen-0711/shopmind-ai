from app.intelligence.deal_detection import DealDetector


def test_detects_lowest_price_as_great_deal():
    detector = DealDetector()

    result = detector.evaluate(
        current_price=52000,
        lowest_price=52000,
        average_price=55000,
    )

    assert result == "Great Deal"


def test_detects_price_below_average_as_good_deal():
    detector = DealDetector()

    result = detector.evaluate(
        current_price=53000,
        lowest_price=50000,
        average_price=55000,
    )

    assert result == "Good Deal"


def test_detects_average_price_as_fair_price():
    detector = DealDetector()

    result = detector.evaluate(
        current_price=55000,
        lowest_price=50000,
        average_price=55000,
    )

    assert result == "Fair Price"


def test_detects_expensive_price():
    detector = DealDetector()

    result = detector.evaluate(
        current_price=60000,
        lowest_price=50000,
        average_price=55000,
    )

    assert result == "Expensive"


def test_missing_price_history_returns_unknown():
    detector = DealDetector()

    result = detector.evaluate(
        current_price=52000,
        lowest_price=None,
        average_price=None,
    )

    assert result == "Unknown"