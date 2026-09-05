
from app.intelligence.price_history import PriceHistory
from app.schemas.product import Product


class ProductRankingService:
    def rank(
        self,
        products: list[Product],
        limit: int | None = None,
        histories: dict[str, PriceHistory] | None = None,
    ) -> list[Product]:

        histories = histories or {}

        def ranking_score(product: Product) -> float:
            rating = product.rating or 0.0
            reviews = product.review_count or 0

            # Quality
            rating_score = (rating / 5.0) * 60.0

            # Review confidence
            review_score = min(reviews / 1000.0, 1.0) * 15.0

            # Price advantage
            if product.price is not None:
                price_score = max(
                    0.0,
                    10.0 - (product.price / 10000.0),
                )
            else:
                price_score = 0.0

            # Historical deal advantage
            deal_score = 0.0

            if product.price is not None:
                history = histories.get(product.title)

                if history is not None:
                    lowest_price = history.lowest_price()

                    if (
                        lowest_price is not None
                        and product.price <= lowest_price
                    ):
                        deal_score = 15.0

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

