class RecommendationEngine:
    """
    Converts product quality and price signals
    into a simple buying recommendation.
    """

    def evaluate(
        self,
        quality_score: float,
        discount: float,
    ) -> str:

        if quality_score >= 90 and discount >= 15:
            return "Strong Buy"

        if quality_score >= 80:
            return "Good Buy"

        if quality_score >= 50:
            return "Consider"

        return "Poor Value"