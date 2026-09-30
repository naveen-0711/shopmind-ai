from app.intelligence.deal_analysis import DealAnalysis
from app.intelligence.price_intelligence import PriceAnalyzer
from app.intelligence.product_scoring import ProductScorer
from app.intelligence.price_history import PriceHistory
from app.intelligence.recommendation import RecommendationEngine


class ProductIntelligenceService:
    """
    Combines product quality, price, deal,
    recommendation, and explanation signals.
    """

    def __init__(self) -> None:
        self.scorer = ProductScorer()
        self.price_analyzer = PriceAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.deal_analysis = DealAnalysis()

    def analyze(
        self,
        rating: float | None,
        review_count: int | None,
        current_price: float | None,
        reference_price: float | None,
    ) -> dict[str, float | str]:

        quality_score = self.scorer.calculate(
            rating=rating,
            review_count=review_count,
        )

        discount_percentage = (
            self.price_analyzer.calculate_discount(
                current_price=current_price,
                reference_price=reference_price,
            )
        )

        recommendation = self.recommendation_engine.evaluate(
            quality_score=quality_score,
            discount=discount_percentage,
        )

        return {
            "quality_score": quality_score,
            "discount_percentage": discount_percentage,
            "recommendation": recommendation,
        }

    def explain(
        self,
        rating: float | None,
        review_count: int | None,
        current_price: float | None,
        reference_price: float | None,
        deal_status: str = "Unknown",
    ) -> dict[str, float | list[str]]:
        """
        Generates a human-readable explanation for
        why a product is recommended.
        """

        analysis = self.analyze(
            rating=rating,
            review_count=review_count,
            current_price=current_price,
            reference_price=reference_price,
        )

        reasons: list[str] = []

        quality_score = float(analysis["quality_score"])
        discount_percentage = float(
            analysis["discount_percentage"]
        )

        # Rating signal
        if rating is not None:
            if rating >= 4.7:
                reasons.append("Excellent customer rating")
            elif rating >= 4.3:
                reasons.append("Strong customer rating")

        # Review credibility signal
        if review_count is not None:
            if review_count >= 5000:
                reasons.append(
                    f"Trusted by {review_count:,}+ reviewers"
                )
            elif review_count >= 500:
                reasons.append(
                    f"Backed by {review_count:,}+ reviews"
                )

        # Price signal
        if discount_percentage > 0:
            reasons.append(
                f"{discount_percentage:.0f}% below the reference price"
            )

        # Deal signal
        normalized_deal_status = deal_status.strip().lower()

        if normalized_deal_status == "great deal":
            reasons.append("Currently a great deal")
        elif normalized_deal_status == "good deal":
            reasons.append("Currently a good deal")

        # Fallback
        if not reasons:
            reasons.append(
                "Matches the available product signals"
            )

        # Combined explainable score
        score = min(
            100.0,
            max(
                0.0,
                quality_score * 0.7
                + min(discount_percentage, 100.0) * 0.3,
            ),
        )

        return {
            "score": round(score, 2),
            "reasons": reasons,
        }

    def analyze_complete(
        self,
        rating: float | None,
        review_count: int | None,
        current_price: float | None,
        reference_price: float | None,
        history: PriceHistory,
    ) -> dict[str, float | str | None]:

        basic_analysis = self.analyze(
            rating=rating,
            review_count=review_count,
            current_price=current_price,
            reference_price=reference_price,
        )

        deal_analysis = self.deal_analysis.analyze(
            current_price=current_price,
            history=history,
        )

        return {
            **basic_analysis,
            **deal_analysis,
        }