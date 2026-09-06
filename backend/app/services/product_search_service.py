from app.ingestion.search_base import ProductSearchProvider
from app.schemas.product import Product

from app.intelligence.deal_analysis import DealAnalysis

from app.services.product_normalization_service import (
    ProductNormalizationService,
)
from app.services.product_ranking_service import (
    ProductRankingService,
)
from app.services.query_parser import QueryParser
from app.services.product_persistence_service import (
    ProductPersistenceService,
)
from app.services.price_history_service import (
    PriceHistoryService,
)


class ProductSearchService:
    def __init__(
        self,
        providers: list[ProductSearchProvider],
        normalization_service: ProductNormalizationService | None = None,
        ranking_service: ProductRankingService | None = None,
        query_parser: QueryParser | None = None,
        persistence_service: ProductPersistenceService | None = None,
        price_history_service: PriceHistoryService | None = None,
    ) -> None:
        self.providers = providers

        self.normalization_service = (
            normalization_service
            if normalization_service is not None
            else ProductNormalizationService()
        )

        self.ranking_service = (
            ranking_service
            if ranking_service is not None
            else ProductRankingService()
        )

        self.query_parser = (
            query_parser
            if query_parser is not None
            else QueryParser()
        )

        self.persistence_service = persistence_service

        self.price_history_service = price_history_service

        self.deal_analysis = DealAnalysis()

    def parse_query(self, query: str):
        return self.query_parser.parse(query)

    def _deduplicate_products(
        self,
        products: list[Product],
    ) -> list[Product]:
        """
        Remove duplicate products using product URL and
        product title as the product identity.
        """

        unique_products: list[Product] = []
        seen: set[tuple[str, str]] = set()

        for product in products:

            product_url = (
                product.product_url.strip().lower()
            )

            product_title = (
                product.title.strip().lower()
            )

            identity = (
                product_url,
                product_title,
            )

            if identity in seen:
                continue

            seen.add(identity)
            unique_products.append(product)

        return unique_products

    async def search(
        self,
        query: str,
        max_price: float | None = None,
        min_rating: float | None = None,
        limit: int = 10,
    ) -> list[Product]:

        # -----------------------------------------
        # 1. Parse natural-language query
        # -----------------------------------------
        parsed_query = self.query_parser.parse(query)

        search_query = parsed_query.product_query

        if max_price is None:
            max_price = parsed_query.max_price

        if min_rating is None:
            min_rating = parsed_query.min_rating

        # -----------------------------------------
        # 2. Search providers
        # -----------------------------------------
        results: list[Product] = []

        for provider in self.providers:

            if not provider.can_search(search_query):
                continue

            raw_products = await provider.search(
                query=search_query,
                max_price=max_price,
                min_rating=min_rating,
                limit=limit,
            )

            for raw_product in raw_products:

                product = self.normalization_service.normalize(
                    raw_product=raw_product,
                    product_url=raw_product["product_url"],
                    source=raw_product["source"],
                )

                results.append(product)

        # -----------------------------------------
        # 3. Apply final filters
        # -----------------------------------------
        filtered_results: list[Product] = []

        for product in results:

            if (
                max_price is not None
                and product.price is not None
                and product.price > max_price
            ):
                continue

            if min_rating is not None:

                if (
                    product.rating is None
                    or product.rating < min_rating
                ):
                    continue

            filtered_results.append(product)

        # -----------------------------------------
        # 4. Remove duplicate products
        # -----------------------------------------
        unique_results = self._deduplicate_products(
            filtered_results
        )

        # -----------------------------------------
        # 5. Rank products
        # -----------------------------------------
        ranked_results = self.ranking_service.rank(
            unique_results,
            limit=limit,
        )

        # -----------------------------------------
        # 6. Persist products + price observations
        # -----------------------------------------
        if self.persistence_service is not None:

            for product in ranked_results:

                self.persistence_service.save_product(
                    title=product.title,
                    product_url=product.product_url,
                    source=product.source,
                    currency=product.currency,
                    rating=product.rating,
                    review_count=product.review_count,
                    image_url=product.image_url,
                    current_price=product.price,
                )

        # -----------------------------------------
        # 7. Analyze price history + deal status
        # -----------------------------------------
        if (
            self.persistence_service is not None
            and self.price_history_service is not None
        ):

            for product in ranked_results:

                saved_product = (
                    self.persistence_service.product_repository.get_by_url(
                        product.product_url
                    )
                )

                if saved_product is None:
                    continue

                history = self.price_history_service.get_history(
                    saved_product.id
                )

                analysis = self.deal_analysis.analyze(
                    current_price=product.price,
                    history=history,
                )

                product.lowest_price = (
                    analysis["lowest_price"]
                )

                product.average_price = (
                    analysis["average_price"]
                )

                product.deal_status = (
                    analysis["deal_status"]
                )

        return ranked_results