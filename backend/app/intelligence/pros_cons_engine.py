from app.schemas.search import ProductSearchProduct


class ProsConsEngine:
    """
    Generates deterministic pros and cons from product signals.

    This engine only uses data that already exists on the product.
    It does not invent specifications, reviews, or product claims.
    """

    def analyze(
        self,
        product: ProductSearchProduct,
    ) -> dict[str, list[str]]:
        pros: list[str] = []
        cons: list[str] = []

        self._analyze_rating(product, pros, cons)
        self._analyze_reviews(product, pros, cons)
        self._analyze_price(product, pros, cons)
        self._analyze_deal(product, pros, cons)
        self._analyze_recommendation(
            product,
            pros,
            cons,
        )
        self._analyze_offers(product, pros, cons)

        return {
            "pros": self._deduplicate(pros),
            "cons": self._deduplicate(cons),
        }

    # ---------------------------------------------------------
    # Rating
    # ---------------------------------------------------------

    def _analyze_rating(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        if product.rating is None:
            return

        if product.rating >= 4.5:
            pros.append(
                f"Excellent {product.rating:.1f}/5 rating."
            )
        elif product.rating >= 4.0:
            pros.append(
                f"Strong {product.rating:.1f}/5 rating."
            )
        elif product.rating < 3.5:
            cons.append(
                f"Low {product.rating:.1f}/5 rating."
            )

    # ---------------------------------------------------------
    # Reviews
    # ---------------------------------------------------------

    def _analyze_reviews(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        if product.review_count is None:
            return

        if product.review_count >= 1000:
            pros.append(
                f"Strong review confidence with "
                f"{product.review_count:,} reviews."
            )
        elif product.review_count < 50:
            cons.append(
                f"Limited review confidence with only "
                f"{product.review_count:,} reviews."
            )

    # ---------------------------------------------------------
    # Price
    # ---------------------------------------------------------

    def _analyze_price(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        if (
            product.price is None
            or product.average_price is None
            or product.average_price <= 0
        ):
            return

        difference_percent = (
            (product.average_price - product.price)
            / product.average_price
        ) * 100

        if difference_percent >= 10:
            pros.append(
                f"Price is about "
                f"{difference_percent:.0f}% below the "
                f"current average."
            )
        elif difference_percent <= -10:
            expensive_percent = abs(difference_percent)

            cons.append(
                f"Price is about "
                f"{expensive_percent:.0f}% above the "
                f"current average."
            )

    # ---------------------------------------------------------
    # Deal status
    # ---------------------------------------------------------

    def _analyze_deal(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        status = (
            product.deal_status.strip().lower()
            if product.deal_status
            else ""
        )

        if status == "great deal":
            pros.append(
                "Currently identified as a great deal."
            )

        elif status == "good deal":
            pros.append(
                "Currently identified as a good deal."
            )

        elif status == "expensive":
            cons.append(
                "Currently priced above the "
                "normal price range."
            )

    # ---------------------------------------------------------
    # ShopMind recommendation score
    # ---------------------------------------------------------

    def _analyze_recommendation(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        if product.recommendation_score is None:
            return

        score = product.recommendation_score

        if score >= 85:
            pros.append(
                f"Strong ShopMind recommendation score "
                f"of {score:.0f}/100."
            )
        elif score >= 75:
            pros.append(
                f"Good ShopMind recommendation score "
                f"of {score:.0f}/100."
            )
        elif score < 50:
            cons.append(
                f"Low ShopMind recommendation score "
                f"of {score:.0f}/100."
            )

    # ---------------------------------------------------------
    # Store offers
    # ---------------------------------------------------------

    def _analyze_offers(
        self,
        product: ProductSearchProduct,
        pros: list[str],
        cons: list[str],
    ) -> None:
        if product.offer_count >= 3:
            pros.append(
                f"Available from {product.offer_count} "
                f"offers, giving you more buying options."
            )
        elif product.offer_count == 1:
            cons.append(
                "Only one offer is currently available."
            )

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _deduplicate(
        items: list[str],
    ) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []

        for item in items:
            normalized = item.strip().lower()

            if not normalized or normalized in seen:
                continue

            seen.add(normalized)
            result.append(item)

        return result