
from abc import ABC, abstractmethod
from typing import Any


class ProductSearchProvider(ABC):
    """
    Base interface for product search providers.
    """

    @abstractmethod
    def can_search(self, query: str) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        pass

