from abc import ABC, abstractmethod
from typing import Any


class ProductAdapter(ABC):
    """
    Base interface for all product source adapters.
    """

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """
        Return True if this adapter can process the given URL.
        """
        pass

    @abstractmethod
    async def fetch_product(self, url: str) -> dict[str, Any]:
        """
        Fetch and return normalized product information.
        """
        pass