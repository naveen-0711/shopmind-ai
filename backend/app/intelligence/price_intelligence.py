class PriceAnalyzer:
    """
    Performs basic price intelligence calculations.
    """

    def calculate_discount(
        self,
        current_price: float | None,
        reference_price: float | None,
    ) -> float:
        """
        Calculate the percentage discount from a reference price.
        """

        if (
            current_price is None
            or reference_price is None
            or reference_price <= 0
        ):
            return 0.0

        if current_price >= reference_price:
            return 0.0

        discount = (
            (reference_price - current_price)
            / reference_price
        ) * 100

        return round(discount, 2)