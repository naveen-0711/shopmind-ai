from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import engine
from app.models.base import Base
from app.models.product import ProductModel


def test_database_can_create_and_query_product():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        product = ProductModel(
            title="iPhone 15",
            product_url="https://amazon.in/example",
            source="amazon",
            currency="INR",
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        assert product.id is not None

        result = session.execute(
            select(ProductModel).where(
                ProductModel.id == product.id
            )
        )

        saved_product = result.scalar_one()

        assert saved_product.title == "iPhone 15"
        assert saved_product.source == "amazon"