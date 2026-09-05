from datetime import datetime

from app.intelligence.product_intelligence import (
    ProductIntelligenceService,
)
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import ProductRepository
from app.services.product_persistence_service import (
    ProductPersistenceService,
)

from tests.test_product_repository import create_test_session


def test_product_analysis_uses_persisted_price_history():
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
        rating=4.5,
        review_count=1000,
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

    assert len(observations) == 3

    intelligence_service = ProductIntelligenceService()

    history_result = intelligence_service.analyze_complete(
        rating=product.rating,
        review_count=product.review_count,
        current_price=52000,
        reference_price=60000,
        history=build_price_history(observations),
    )

    assert history_result["lowest_price"] == 52000
    assert history_result["average_price"] == 55666.67
    assert history_result["deal_status"] == "Great Deal"

    session.close()


def build_price_history(observations):
    from app.intelligence.price_history import PriceHistory

    history = PriceHistory()

    for observation in observations:
        history.add(
            price=observation.price,
            observed_at=observation.observed_at,
        )

    return history