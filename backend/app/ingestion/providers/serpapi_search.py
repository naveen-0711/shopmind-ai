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

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    async def _request_immersive_product(
        self,
        page_token: str,
    ) -> dict[str, Any]:
        """
        Request Google Immersive Product API data.
        """
        params = {
            "engine": "google_immersive_product",
            "page_token": page_token,
            "api_key": self.api_key,
            "gl": self.country,
            "hl": "en",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    def _extract_direct_retailer_url(
        self,
        seller: dict[str, Any],
    ) -> str | None:
        """
        Extract a direct retailer URL.

        Supports the direct_link field used by seller-style
        responses and returns None when it is missing/empty.
        """
        direct_link = seller.get("direct_link")

        if not isinstance(direct_link, str):
            return None

        direct_link = direct_link.strip()

        if not direct_link:
            return None

        return direct_link

    def _extract_best_retailer_url(
        self,
        sellers: list[dict[str, Any]],
    ) -> str | None:
        """
        Return the first valid direct retailer URL.
        """
        for seller in sellers:
            if not isinstance(seller, dict):
                continue

            direct_link = self._extract_direct_retailer_url(
                seller
            )

            if direct_link is not None:
                return direct_link

        return None

    def _extract_store_url(
        self,
        store: dict[str, Any],
    ) -> str | None:
        """
        Extract the retailer URL from an Immersive Product
        API store result.

        Immersive Product API uses `link` for the retailer
        store URL.
        """
        link = store.get("link")

        if not isinstance(link, str):
            return None

        link = link.strip()

        if not link:
            return None

        return link

    def _extract_best_store_url(
        self,
        stores: list[dict[str, Any]],
    ) -> str | None:
        """
        Return the first valid retailer store URL.
        """
        for store in stores:
            if not isinstance(store, dict):
                continue

            link = self._extract_store_url(store)

            if link is not None:
                return link

        return None

    async def _resolve_retailer_url(
        self,
        page_token: str,
        source: str,
    ) -> str | None:
        """
        Resolve a Google Shopping product to a direct
        retailer URL using the Immersive Product API.
        """
        try:
            data = await self._request_immersive_product(
                page_token
            )
        except Exception:
            return None

        product_results = data.get(
            "product_results",
            {},
        )

        if not isinstance(product_results, dict):
            return None

        stores = product_results.get(
            "stores",
            [],
        )

        if not isinstance(stores, list):
            return None

        normalized_source = source.strip().lower()

        # First try to find the exact retailer.
        for store in stores:
            if not isinstance(store, dict):
                continue

            store_name = store.get("name", "")

            if (
                isinstance(store_name, str)
                and store_name.strip().lower()
                == normalized_source
            ):
                retailer_url = self._extract_store_url(
                    store
                )

                if retailer_url is not None:
                    return retailer_url

        # If the requested retailer is not found,
        # use the first available retailer.
        return self._extract_best_store_url(stores)

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

        if not isinstance(shopping_results, list):
            return []

        products: list[dict[str, Any]] = []

        for item in shopping_results:
            if not isinstance(item, dict):
                continue

            title = item.get(
                "title",
                "",
            ).strip()

            price = item.get(
                "extracted_price"
            )

            # Skip products with unusable data.
            if not title:
                continue

            if price is None or price <= 0:
                continue

            # Maximum price filter.
            if (
                max_price is not None
                and price > max_price
            ):
                continue

            rating = item.get("rating")

            # Minimum rating filter.
            if min_rating is not None:
                if (
                    rating is None
                    or rating < min_rating
                ):
                    continue

            # Original Google Shopping URL.
            # This is always our safe fallback.
            product_url = (
                item.get("product_link")
                or item.get("link")
                or ""
            )

            if not product_url:
                continue

            # Resolve the actual retailer URL when
            # Google provides an immersive product token.
            page_token = item.get(
                "immersive_product_page_token"
            )

            if page_token:
                retailer_url = await self._resolve_retailer_url(
                    page_token=page_token,
                    source=item.get(
                        "source",
                        "",
                    ),
                )

                if retailer_url:
                    product_url = retailer_url

            products.append(
                {
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "review_count": item.get(
                        "reviews"
                    ),
                    "image_url": item.get(
                        "thumbnail"
                    ),
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