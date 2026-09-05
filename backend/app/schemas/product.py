from pydantic import BaseModel, Field, HttpUrl


class ProductAnalyzeRequest(BaseModel):
    url: HttpUrl


class Product(BaseModel):
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