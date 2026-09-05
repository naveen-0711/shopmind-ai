from app.intelligence.deal_analysis import DealAnalysis
from app.intelligence.price_intelligence import PriceAnalyzer
from app.intelligence.product_scoring import ProductScorer
from app.intelligence.price_history import PriceHistory
from app.intelligence.recommendation import RecommendationEngine


class ProductIntelligenceService:
    """
    Combines product quality, price, deal,
    and recommendation signals.
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