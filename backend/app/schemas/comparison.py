from pydantic import BaseModel, Field


class ComparisonProduct(BaseModel):
    title: str
    price: float | None = None
    currency: str = "INR"
    rating: float | None = None
    review_count: int | None = None
    image_url: str | None = None
    product_url: str
    source: str

    lowest_price: float | None = None
    average_price: float | None = None
    deal_status: str = "Unknown"

    offers: list = Field(default_factory=list)
    offer_count: int = 0
    savings: float | None = None

    recommendation_score: float | None = None
    recommendation_reasons: list[str] = Field(
        default_factory=list
    )


class ProductComparisonSummary(BaseModel):
    best_overall: ComparisonProduct | None = None
    best_value: ComparisonProduct | None = None
    cheapest: ComparisonProduct | None = None
    best_rated: ComparisonProduct | None = None
    best_deal: ComparisonProduct | None = None