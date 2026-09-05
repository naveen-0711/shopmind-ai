class DealDetector:
    """
    Evaluates the current product price against
    historical price information.
    """

    def evaluate(
        self,
        current_price: float | None,
        lowest_price: float | None,
        average_price: float | None,
    ) -> str:

        if (
            current_price is None
            or lowest_price is None
            or average_price is None
        ):
            return "Unknown"

        if current_price <= lowest_price:
            return "Great Deal"

        if current_price < average_price:
            return "Good Deal"

        if current_price == average_price:
            return "Fair Price"

        return "Expensive"