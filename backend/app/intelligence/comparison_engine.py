from app.schemas.search import ProductSearchProduct


class ComparisonEngine:
    """
    Compares products using ShopMind's existing
    recommendation, price, rating, review and deal signals.
    """

    def compare(
        self,
        products: list[ProductSearchProduct],
    ) -> dict:
        if not products:
            return {
                "best_overall": None,
                "best_value": None,
                "cheapest": None,
                "best_rated": None,
                "best_deal": None,
            }

        return {
            "best_overall": self._best_overall(products),
            "best_value": self._best_value(products),
            "cheapest": self._cheapest(products),
            "best_rated": self._best_rated(products),
            "best_deal": self._best_deal(products),
        }

    def _best_overall(
        self,
        products: list[ProductSearchProduct],
    ) -> ProductSearchProduct:
        return max(
            products,
            key=self._overall_score,
        )

    def _overall_score(
        self,
        product: ProductSearchProduct,
    ) -> float:
        recommendation_score = (
            product.recommendation_score
            if product.recommendation_score is not None
            else 0
        )

        rating = product.rating or 0
        reviews = product.review_count or 0

        review_confidence = min(
            10,
            reviews / 1000,
        )

        return (
            recommendation_score * 0.75
            + rating * 3
            + review_confidence
        )

    def _best_value(
        self,
        products: list[ProductSearchProduct],
    ) -> ProductSearchProduct:
        valid_prices = [
            product.price
            for product in products
            if product.price is not None
        ]

        if not valid_prices:
            return self._best_overall(products)

        cheapest_price = min(valid_prices)

        def value_score(
            product: ProductSearchProduct,
        ) -> float:
            recommendation_score = (
                product.recommendation_score
                if product.recommendation_score is not None
                else 0
            )

            if product.price is None:
                return -1

            price_advantage = (
                cheapest_price / product.price
            ) * 100

            return (
                recommendation_score * 0.65
                + price_advantage * 0.35
            )

        return max(
            products,
            key=value_score,
        )

    def _cheapest(
        self,
        products: list[ProductSearchProduct],
    ) -> ProductSearchProduct | None:
        priced_products = [
            product
            for product in products
            if product.price is not None
        ]

        if not priced_products:
            return None

        return min(
            priced_products,
            key=lambda product: product.price,
        )

    def _best_rated(
        self,
        products: list[ProductSearchProduct],
    ) -> ProductSearchProduct | None:
        rated_products = [
            product
            for product in products
            if product.rating is not None
        ]

        if not rated_products:
            return None

        return max(
            rated_products,
            key=lambda product: (
                product.rating,
                product.review_count or 0,
            ),
        )

    def _best_deal(
        self,
        products: list[ProductSearchProduct],
    ) -> ProductSearchProduct | None:
        deal_priority = {
            "great deal": 3,
            "good deal": 2,
            "fair price": 1,
            "unknown": 0,
        }

        return max(
            products,
            key=lambda product: (
                deal_priority.get(
                    product.deal_status.strip().lower(),
                    0,
                ),
                product.savings or 0,
            ),
        )