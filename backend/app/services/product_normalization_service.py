from typing import Any

from app.schemas.product import Product


class ProductNormalizationService:
    """
    Converts raw marketplace product data
    into the canonical Product schema.
    """

    def normalize(
        self,
        raw_product: dict[str, Any],
        product_url: str,
        source: str,
    ) -> Product:

        return Product(
            title=raw_product["title"],
            price=(
                float(raw_product["price"])
                if raw_product.get("price") is not None
                else None
            ),
            currency=raw_product.get("currency", "INR"),
            rating=(
                float(raw_product["rating"])
                if raw_product.get("rating") is not None
                else None
            ),
            review_count=(
                int(raw_product["review_count"])
                if raw_product.get("review_count") is not None
                else None
            ),
            image_url=raw_product.get("image_url"),
            product_url=product_url,
            source=source,
        )

