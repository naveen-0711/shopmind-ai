from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.base import Base
from app.models.product import ProductModel
from app.repositories.product_repository import ProductRepository
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)


def create_test_session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def create_product(session):
    product = ProductModel(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


def test_repository_creates_price_observation():
    session = create_test_session()
    product = create_product(session)

    repository = PriceObservationRepository(session)

    observation = repository.create(
        product_id=product.id,
        price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    assert observation.id is not None
    assert observation.product_id == product.id
    assert observation.price == 52000
    assert observation.observed_at == datetime(2026, 9, 3)

    session.close()


def test_repository_gets_price_observations_for_product():
    session = create_test_session()
    product = create_product(session)

    repository = PriceObservationRepository(session)

    repository.create(
        product_id=product.id,
        price=60000,
        observed_at=datetime(2026, 9, 1),
    )

    repository.create(
        product_id=product.id,
        price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    observations = repository.get_for_product(
        product.id
    )

    assert len(observations) == 2
    assert observations[0].price == 60000
    assert observations[1].price == 52000

    session.close()


def test_repository_returns_empty_list_for_product_without_history():
    session = create_test_session()
    product = create_product(session)

    repository = PriceObservationRepository(session)

    observations = repository.get_for_product(
        product.id
    )

    assert observations == []

    session.close()

def test_get_for_product_returns_observations_in_time_order():
    from datetime import datetime

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
        price=50000,
        observed_at=datetime(2026, 9, 3),
    )

    price_repository.create(
        product_id=product.id,
        price=55000,
        observed_at=datetime(2026, 9, 1),
    )

    price_repository.create(
        product_id=product.id,
        price=52000,
        observed_at=datetime(2026, 9, 2),
    )

    observations = price_repository.get_for_product(
        product.id
    )

    assert len(observations) == 3

    assert observations[0].price == 55000
    assert observations[1].price == 52000
    assert observations[2].price == 50000

    session.close()