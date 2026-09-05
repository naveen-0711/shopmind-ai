from typing import Any

from app.ingestion.base import ProductAdapter
from app.ingestion.http_client import ProductHttpClient
from app.ingestion.parser import ProductParser
from app.schemas.product import Product


class AmazonAdapter(ProductAdapter):
    """
    Adapter for Amazon product URLs.
    """

    def __init__(self) -> None:
        self.http_client = ProductHttpClient()
        self.parser = ProductParser()

    def can_handle(self, url: str) -> bool:
        return (
            "amazon.in" in url.lower()
            or "amazon.com" in url.lower()
        )

    async def fetch_product(self, url: str) -> dict[str, Any]:
        """
        Fetch Amazon HTML and extract product information.
        """

        html = await self.http_client.fetch(url)

        return self.parser.parse(html)

    async def normalize_product(
        self,
        raw_data: dict[str, Any],
        url: str,
    ) -> Product:
        """
        Convert raw Amazon data into the common Product schema.
        """

        price = raw_data.get("price")
        rating = raw_data.get("rating")
        review_count = raw_data.get("review_count")

        return Product(
            title=raw_data["title"],
            price=float(price) if price is not None else None,
            currency="INR",
            rating=float(rating) if rating is not None else None,
            review_count=(
                int(review_count)
                if review_count is not None
                else None
            ),
            image_url=raw_data.get("image_url"),
            product_url=url,
            source="amazon",
        )