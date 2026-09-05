from app.ingestion.resolver import ProductResolver
from app.schemas.product import Product


class ProductService:
    """
    Business logic for analyzing products.
    """

    def __init__(self, resolver: ProductResolver):
        self.resolver = resolver

    async def analyze_product(self, url: str) -> Product:
        """
        Resolve the URL, fetch raw product data,
        and normalize it into a Product.
        """

        adapter = self.resolver.resolve(url)

        if adapter is None:
            raise ValueError("Unsupported product URL")

        raw_data = await adapter.fetch_product(url)

        product = await adapter.normalize_product(
            raw_data,
            url,
        )

        return product