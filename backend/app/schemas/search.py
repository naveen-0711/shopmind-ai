from pydantic import BaseModel, Field

from app.schemas.offer import ProductOffer
from app.schemas.query import ParsedSearchQuery
from app.schemas.comparison import ProductComparisonSummary


class ProductSearchRequest(BaseModel):
    query: str = Field(min_length=1)

    max_price: float | None = Field(
        default=None,
        gt=0,
    )

    min_rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=50,
    )


class ProductSearchProduct(BaseModel):
    """
    API representation of a product together with
    its marketplace offers.
    """

    title: str

    price: float | None = None

    currency: str = "INR"

    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )

    review_count: int | None = Field(
        default=None,
        ge=0,
    )

    image_url: str | None = None

    product_url: str

    source: str

    lowest_price: float | None = None

    average_price: float | None = None

    deal_status: str = "Unknown"

    offers: list[ProductOffer] = Field(
        default_factory=list,
    )

    offer_count: int = 0

    savings: float | None = None

    recommendation_score: float | None = None

    recommendation_reasons: list[str] = Field(default_factory=list)
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)


class ProductSearchResponse(BaseModel):
    query: str
    interpreted_query: ParsedSearchQuery | None = None
    products: list[ProductSearchProduct]
    total: int
    comparison: ProductComparisonSummary | None = None