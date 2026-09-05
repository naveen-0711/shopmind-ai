from pydantic import BaseModel, Field

from app.schemas.query import ParsedSearchQuery


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


class ProductSearchResponse(BaseModel):
    query: str
    interpreted_query: ParsedSearchQuery | None = None
    products: list[dict]
    total: int
