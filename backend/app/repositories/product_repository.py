from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import ProductModel


class ProductRepository:
    """
    Handles database operations for products.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        title: str,
        product_url: str,
        source: str,
        currency: str = "INR",
        rating: float | None = None,
        review_count: int | None = None,
        image_url: str | None = None,
    ) -> ProductModel:

        product = ProductModel(
            title=title,
            product_url=product_url,
            source=source,
            currency=currency,
            rating=rating,
            review_count=review_count,
            image_url=image_url,
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def get_by_url(
        self,
        product_url: str,
    ) -> ProductModel | None:

        statement = select(ProductModel).where(
            ProductModel.product_url == product_url
        )

        result = self.session.execute(statement)

        return result.scalar_one_or_none()