from app.intelligence.price_history import PriceHistory
from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)


class PriceHistoryService:
    """
    Reconstructs PriceHistory from persisted price observations.
    """

    def __init__(
        self,
        price_repository: PriceObservationRepository,
    ) -> None:
        self.price_repository = price_repository

    def get_history(
        self,
        product_id: int,
    ) -> PriceHistory:

        observations = self.price_repository.get_for_product(
            product_id
        )

        history = PriceHistory()

        for observation in observations:
            history.add(
                price=observation.price,
                observed_at=observation.observed_at,
            )

        return history