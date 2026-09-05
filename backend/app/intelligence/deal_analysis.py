from app.intelligence.deal_detection import DealDetector
from app.intelligence.price_history import PriceHistory


class DealAnalysis:
    """
    Combines price history with deal detection.
    """

    def __init__(self) -> None:
        self.detector = DealDetector()

    def analyze(
        self,
        current_price: float | None,
        history: PriceHistory,
    ) -> dict[str, float | str | None]:

        lowest_price = history.lowest_price()
        average_price = history.average_price()

        average_price = (
            round(average_price, 2)
            if average_price is not None
            else None
        )

        deal_status = self.detector.evaluate(
            current_price=current_price,
            lowest_price=lowest_price,
            average_price=average_price,
        )

        return {
            "lowest_price": lowest_price,
            "average_price": average_price,
            "deal_status": deal_status,
        }