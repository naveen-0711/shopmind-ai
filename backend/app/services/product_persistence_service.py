from datetime import datetime

from app.models.product import ProductModel
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import ProductRepository


class ProductPersistenceService:
    """
    Persists products and their current price observations.
    """

    def __init__(
        self,
        product_repository: ProductRepository,
        price_repository: PriceObservationRepository,
    ) -> None:
        self.product_repository = product_repository
        self.price_repository = price_repository

    def save_product(
        self,
        title: str,
        product_url: str,
        source: str,
        currency: str = "INR",
        rating: float | None = None,
        review_count: int | None = None,
        image_url: str | None = None,
        current_price: float | None = None,
        observed_at: datetime | None = None,
    ) -> ProductModel:
        product = self.product_repository.get_by_url(product_url)

        if product is None:
            product = self.product_repository.create(
                title=title,
                product_url=product_url,
                source=source,
                currency=currency,
                rating=rating,
                review_count=review_count,
                image_url=image_url,
            )

        if current_price is not None:
            observation_time = (
                observed_at
                if observed_at is not None
                else datetime.now()
            )

            self.price_repository.create(
                product_id=product.id,
                price=current_price,
                observed_at=observation_time,
            )

        return product
