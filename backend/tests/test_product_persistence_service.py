from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.base import Base
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import ProductRepository
from app.services.product_persistence_service import (
    ProductPersistenceService,
)


def create_test_session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def test_persistence_service_saves_product_and_price():
    session = create_test_session()

    product_repository = ProductRepository(session)
    price_repository = PriceObservationRepository(session)

    service = ProductPersistenceService(
        product_repository=product_repository,
        price_repository=price_repository,
    )

    product = service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        rating=4.5,
        review_count=1000,
        image_url="https://example.com/iphone.jpg",
        current_price=52000,
        observed_at=datetime(2026, 9, 5, 12, 0, 0),
    )

    assert product.id is not None
    assert product.title == "iPhone 15"

    observations = price_repository.get_for_product(
        product.id
    )

    assert len(observations) == 1
    assert observations[0].price == 52000
    assert observations[0].observed_at == datetime(
        2026,
        9,
        5,
        12,
        0,
        0,
    )

    session.close()


def test_persistence_service_does_not_save_missing_price():
    session = create_test_session()

    product_repository = ProductRepository(session)
    price_repository = PriceObservationRepository(session)

    service = ProductPersistenceService(
        product_repository=product_repository,
        price_repository=price_repository,
    )

    product = service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        current_price=None,
        observed_at=datetime(2026, 9, 5, 12, 0, 0),
    )

    observations = price_repository.get_for_product(
        product.id
    )

    assert observations == []

    session.close()
def test_persistence_service_reuses_existing_product():
    session = create_test_session()

    product_repository = ProductRepository(session)
    price_repository = PriceObservationRepository(session)

    service = ProductPersistenceService(
        product_repository=product_repository,
        price_repository=price_repository,
    )

    first_product = service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        current_price=60000,
        observed_at=datetime(2026, 9, 1),
    )

    second_product = service.save_product(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        current_price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    assert second_product.id == first_product.id

    observations = price_repository.get_for_product(
        first_product.id
    )

    assert len(observations) == 2
    assert observations[0].price == 60000
    assert observations[1].price == 52000

    session.close()