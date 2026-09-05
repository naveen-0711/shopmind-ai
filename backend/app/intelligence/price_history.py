from datetime import datetime


class PriceHistory:
    """
    Stores and analyzes price observations.
    """

    def __init__(self) -> None:
        self.observations: list[dict] = []

    def add(
        self,
        price: float,
        observed_at: datetime,
    ) -> None:
        self.observations.append(
            {
                "price": price,
                "observed_at": observed_at,
            }
        )

    def lowest_price(self) -> float | None:
        if not self.observations:
            return None

        return min(
            observation["price"]
            for observation in self.observations
        )

    def average_price(self) -> float | None:
        if not self.observations:
            return None

        total = sum(
            observation["price"]
            for observation in self.observations
        )

        return total / len(self.observations)

    def recent(
        self,
        since: datetime,
    ) -> list[dict]:
        return [
            observation
            for observation in self.observations
            if observation["observed_at"] >= since
        ]