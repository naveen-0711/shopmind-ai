from app.intelligence.price_history import PriceHistory
from app.schemas.product import Product


class ProductRankingService:
    """
    Ranks products using quality, popularity, price,
    and deal signals.
    """

    def rank(
        self,
        products: list[Product],
        limit: int | None = None,
        histories: dict[str, PriceHistory] | None = None,
    ) -> list[Product]:

        histories = histories or {}

        def ranking_score(product: Product) -> float:
            # -----------------------------------------
            # 1. Rating quality
            # -----------------------------------------
            rating = product.rating or 0.0

            rating_score = (
                rating / 5.0
            ) * 50.0

            # -----------------------------------------
            # 2. Review confidence
            # -----------------------------------------
            reviews = product.review_count or 0

            review_score = (
                min(reviews / 1000.0, 1.0)
            ) * 20.0

            # -----------------------------------------
            # 3. Price competitiveness
            # -----------------------------------------
            if product.price is not None:
                price_score = max(
                    0.0,
                    15.0 - (
                        product.price / 10000.0
                    ),
                )
            else:
                price_score = 0.0

            # -----------------------------------------
            # 4. Deal status
            # -----------------------------------------
            deal_score = 0.0

            deal_scores = {
                "Great Deal": 15.0,
                "Good Deal": 10.0,
                "Fair Price": 5.0,
                "Expensive": 0.0,
                "Unknown": 0.0,
            }

            deal_score = deal_scores.get(
                product.deal_status,
                0.0,
            )

            # -----------------------------------------
            # 5. Historical price advantage
            #
            # Kept for future ranking integration.
            # -----------------------------------------
            if product.price is not None:

                history = histories.get(
                    product.title
                )

                if history is not None:

                    lowest_price = (
                        history.lowest_price()
                    )

                    if (
                        lowest_price is not None
                        and product.price <= lowest_price
                    ):
                        deal_score = max(
                            deal_score,
                            15.0,
                        )

            return (
                rating_score
                + review_score
                + price_score
                + deal_score
            )

        ranked_products = sorted(
            products,
            key=ranking_score,
            reverse=True,
        )

        if limit is not None:
            return ranked_products[:limit]

        return ranked_products