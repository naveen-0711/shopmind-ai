class ProductScorer:
    """
    Calculates a simple product quality score from
    rating and review count.
    """

    def calculate(
        self,
        rating: float | None,
        review_count: int | None,
    ) -> float:

        if rating is None:
            return 0.0

        # Rating contributes up to 80 points.
        rating_score = (rating / 5.0) * 80.0

        # Reviews contribute up to 20 points.
        # 1000+ reviews gives the full review score.
        reviews = review_count or 0

        review_score = min(reviews / 1000.0, 1.0) * 20.0

        score = rating_score + review_score

        return round(
            min(max(score, 0.0), 100.0),
            2,
        )