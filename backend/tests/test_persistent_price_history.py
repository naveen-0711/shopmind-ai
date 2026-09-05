from datetime import datetime

from app.intelligence.price_history import PriceHistory
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import ProductRepository
from app.services.product_persistence_service import (
    ProductPersistenceService,
)

from tests.test_product_repository import create_test_session


def test_database_observations_can_rebuild_price_history():
    session = create_test_session()

    product_repository = ProductRepository(session)
    price_repository = PriceObservationRepository(session)

    persistence_service = ProductPersistenceService(
        product_repository=product_repository,
        price_repository=price_repository,
    )

    product = persistence_service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/iphone-15",
        source="amazon",
        currency="INR",
        current_price=60000,
        observed_at=datetime(2026, 9, 1),
    )

    persistence_service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/iphone-15",
        source="amazon",
        currency="INR",
        current_price=55000,
        observed_at=datetime(2026, 9, 2),
    )

    persistence_service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/iphone-15",
        source="amazon",
        currency="INR",
        current_price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    observations = price_repository.get_for_product(
        product.id
    )

    history = PriceHistory()

    for observation in observations:
        history.add(
            price=observation.price,
            observed_at=observation.observed_at,
        )

    assert len(history.observations) == 3
    assert history.lowest_price() == 52000
    assert history.average_price() == 55666.666666666664

    session.close()