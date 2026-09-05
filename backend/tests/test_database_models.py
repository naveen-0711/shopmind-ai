from datetime import datetime

from app.models.product import ProductModel
from app.models.price_observation import PriceObservation


def test_product_model_contains_required_fields():
    product = ProductModel(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
        rating=4.5,
        review_count=1000,
        image_url="https://example.com/image.jpg",
    )

    assert product.title == "iPhone 15"
    assert product.product_url == "https://amazon.in/example"
    assert product.source == "amazon"
    assert product.currency == "INR"
    assert product.rating == 4.5
    assert product.review_count == 1000


def test_price_observation_contains_price_and_timestamp():
    observed_at = datetime(2026, 9, 3)

    observation = PriceObservation(
        price=52000,
        observed_at=observed_at,
    )

    assert observation.price == 52000
    assert observation.observed_at == observed_at

def test_product_has_price_observations():
    product = ProductModel(
        title="iPhone 15",
        product_url="https://amazon.in/example",
        source="amazon",
        currency="INR",
    )

    observation = PriceObservation(
        price=52000,
        observed_at=datetime(2026, 9, 3),
    )

    product.price_observations.append(observation)

    assert len(product.price_observations) == 1
    assert product.price_observations[0].price == 52000
    assert product.price_observations[0].observed_at == datetime(
        2026, 9, 3
    )