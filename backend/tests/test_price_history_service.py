from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import ProductRepository
from app.services.price_history_service import PriceHistoryService

from tests.test_product_repository import create_test_session


def test_price_history_service_builds_history_from_database():
    session = create_test_session()

    product_repository = ProductRepository(session)
    price_repository = PriceObservationRepository(session)

    product = product_repository.create(
        title="iPhone 15",
        product_url="https://amazon.in/iphone-15",
        source="amazon",
        currency="INR",
    )

    price_repository.create(
        product_id=product.id,
        price=60000,
        observed_at=datetime(2026, 9, 1),
    )

    price_repository.create(
        product_id=product.id,
        price=55000,
        observed_at=datetime(2026, 9, 2),
    )

    price_repository.create(
        product_id=product.id,
        price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    service = PriceHistoryService(
        price_repository=price_repository,
    )

    history = service.get_history(product.id)

    assert isinstance(history, PriceHistory)
    assert len(history.observations) == 3
    assert history.lowest_price() == 52000
    assert history.average_price() == 55666.666666666664

    assert history.observations[0]["price"] == 60000
    assert history.observations[1]["price"] == 55000
    assert history.observations[2]["price"] == 52000

    session.close()