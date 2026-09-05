from typing import Any

import httpx

from app.ingestion.search_base import ProductSearchProvider


class SerpApiSearchProvider(ProductSearchProvider):
    BASE_URL = "https://serpapi.com/search.json"

    def __init__(
        self,
        api_key: str,
        country: str = "in",
    ) -> None:
        self.api_key = api_key
        self.country = country

    def can_search(self, query: str) -> bool:
        return bool(query.strip())

    async def _request(
        self,
        query: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": self.api_key,
            "gl": self.country,
            "hl": "en",
            "num": limit,
        }

        async with httpx.AsyncClient(
            timeout=15.0,
        ) as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        data = await self._request(
            query=query,
            limit=limit,
        )

        shopping_results = data.get(
            "shopping_results",
            [],
        )

        products: list[dict[str, Any]] = []

        for item in shopping_results:
            title = item.get("title", "").strip()
            price = item.get("extracted_price")

            # Skip products with unusable data.
            if not title:
                continue

            if price is None or price <= 0:
                continue

            # Apply maximum price filter.
            if (
                max_price is not None
                and price > max_price
            ):
                continue

            rating = item.get("rating")

            # When a minimum rating is requested,
            # unrated products must not be returned.
            if min_rating is not None:
                if rating is None or rating < min_rating:
                    continue

            product_url = (
                item.get("product_link")
                or item.get("link")
                or ""
            )

            # Skip products without a usable URL.
            if not product_url:
                continue

            products.append(
                {
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "review_count": item.get("reviews"),
                    "image_url": item.get("thumbnail"),
                    "product_url": product_url,
                    "source": item.get(
                        "source",
                        "Google Shopping",
                    ),
                    "currency": "INR",
                }
            )

            if len(products) >= limit:
                break

        return products
