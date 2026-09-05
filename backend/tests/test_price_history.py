from datetime import datetime, timedelta

from app.intelligence.price_history import PriceHistory


def test_adds_price_observation():
    history = PriceHistory()

    history.add(
        price=54000,
        observed_at=datetime(2026, 9, 1),
    )

    assert len(history.observations) == 1
    assert history.observations[0]["price"] == 54000


def test_returns_lowest_price():
    history = PriceHistory()

    history.add(55000, datetime(2026, 9, 1))
    history.add(52000, datetime(2026, 9, 2))
    history.add(54000, datetime(2026, 9, 3))

    assert history.lowest_price() == 52000


def test_returns_average_price():
    history = PriceHistory()

    history.add(50000, datetime(2026, 9, 1))
    history.add(60000, datetime(2026, 9, 2))

    assert history.average_price() == 55000


def test_returns_none_when_history_is_empty():
    history = PriceHistory()

    assert history.lowest_price() is None
    assert history.average_price() is None


def test_returns_recent_observations():
    history = PriceHistory()

    history.add(50000, datetime(2026, 8, 1))
    history.add(52000, datetime(2026, 9, 1))
    history.add(54000, datetime(2026, 9, 3))

    result = history.recent(
        since=datetime(2026, 9, 1)
    )

    assert len(result) == 2
    assert result[0]["price"] == 52000
    assert result[1]["price"] == 54000