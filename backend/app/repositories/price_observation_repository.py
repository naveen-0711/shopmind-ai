from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.price_observation import PriceObservation


class PriceObservationRepository:
    """
    Handles database operations for price observations.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        product_id: int,
        price: float,
        observed_at: datetime,
    ) -> PriceObservation:

        observation = PriceObservation(
            product_id=product_id,
            price=price,
            observed_at=observed_at,
        )

        self.session.add(observation)
        self.session.commit()
        self.session.refresh(observation)

        return observation

    def get_for_product(
        self,
        product_id: int,
    ) -> list[PriceObservation]:

        statement = (
            select(PriceObservation)
            .where(
                PriceObservation.product_id == product_id
            )
            .order_by(
                PriceObservation.observed_at
            )
        )

        result = self.session.execute(statement)

        return list(result.scalars().all())