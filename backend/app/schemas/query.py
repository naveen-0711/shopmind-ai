
from pydantic import BaseModel, Field


class ParsedSearchQuery(BaseModel):
    product_query: str = Field(min_length=1)
    max_price: float | None = Field(
        default=None,
        gt=0,
    )
    min_price: float | None = Field(
        default=None,
        gt=0,
    )
    min_rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )

