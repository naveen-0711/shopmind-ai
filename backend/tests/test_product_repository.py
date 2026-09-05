from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.base import Base
from app.repositories.product_repository import ProductRepository


def create_test_session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def test_repository_creates_product():
    session = create_test_session()
    repository = ProductRepository(session)

    product = repository.create(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        rating=4.5,
        review_count=1000,
        image_url="https://example.com/iphone.jpg",
    )

    assert product.id is not None
    assert product.title == "iPhone 15"
    assert product.source == "amazon"

    session.close()


def test_repository_finds_product_by_url():
    session = create_test_session()
    repository = ProductRepository(session)

    repository.create(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
    )

    product = repository.get_by_url(
        "https://amazon.in/example"
    )

    assert product is not None
    assert product.title == "iPhone 15"

    session.close()


def test_repository_returns_none_for_unknown_url():
    session = create_test_session()
    repository = ProductRepository(session)

    product = repository.get_by_url(
        "https://amazon.in/does-not-exist"
    )

    assert product is None

    session.close()