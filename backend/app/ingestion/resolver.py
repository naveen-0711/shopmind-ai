from app.ingestion.base import ProductAdapter
from app.ingestion.adapters.amazon import AmazonAdapter


class ProductResolver:
    """
    Resolves a product URL to the appropriate product adapter.
    """

    def __init__(self) -> None:
        self.adapters: list[ProductAdapter] = [
            AmazonAdapter(),
        ]

    def resolve(self, url: str) -> ProductAdapter | None:
        """
        Return the adapter capable of handling the URL.
        """
        for adapter in self.adapters:
            if adapter.can_handle(url):
                return adapter

        return None