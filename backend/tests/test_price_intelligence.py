from app.intelligence.price_intelligence import PriceAnalyzer


def test_calculates_discount_percentage():
    analyzer = PriceAnalyzer()

    discount = analyzer.calculate_discount(
        current_price=54000,
        reference_price=60000,
    )

    assert discount == 10.0


def test_calculates_zero_discount_when_prices_are_equal():
    analyzer = PriceAnalyzer()

    discount = analyzer.calculate_discount(
        current_price=60000,
        reference_price=60000,
    )

    assert discount == 0.0


def test_returns_zero_when_reference_price_is_missing():
    analyzer = PriceAnalyzer()

    discount = analyzer.calculate_discount(
        current_price=54000,
        reference_price=None,
    )

    assert discount == 0.0


def test_returns_zero_when_reference_price_is_zero():
    analyzer = PriceAnalyzer()

    discount = analyzer.calculate_discount(
        current_price=54000,
        reference_price=0,
    )

    assert discount == 0.0


def test_discount_does_not_become_negative():
    analyzer = PriceAnalyzer()

    discount = analyzer.calculate_discount(
        current_price=65000,
        reference_price=60000,
    )

    assert discount == 0.0