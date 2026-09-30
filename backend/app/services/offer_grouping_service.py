from app.schemas.offer import (
    GroupedProduct,
    ProductOffer,
)
from app.schemas.product import Product
from app.services.product_identity_service import (
    ProductIdentityService,
)


class OfferGroupingService:
    """
    Groups marketplace offers that represent the same product.
    """

    def __init__(
        self,
        identity_service: ProductIdentityService | None = None,
    ) -> None:
        self.identity_service = (
            identity_service
            if identity_service is not None
            else ProductIdentityService()
        )

    def group(
        self,
        products: list[Product],
    ) -> dict[str, list[Product]]:
        """
        Group products using their normalized title.
        """

        groups: dict[str, list[Product]] = {}

        for product in products:

            identity = (
                self.identity_service.normalize_title(
                    product.title
                )
            )

            if identity not in groups:
                groups[identity] = []

            groups[identity].append(product)

        return groups

    def best_offer(
        self,
        products: list[Product],
    ) -> Product | None:
        """
        Return the cheapest valid offer.
        """

        valid_products = [
            product
            for product in products
            if product.price is not None
        ]

        if not valid_products:
            return None

        return min(
            valid_products,
            key=lambda product: product.price,
        )

    def create_grouped_product(
        self,
        products: list[Product],
    ) -> GroupedProduct | None:
        """
        Convert multiple offers for the same product
        into a single grouped product.
        """

        if not products:
            return None

        best = self.best_offer(products)

        if best is None:
            return None

        offers = [
            ProductOffer(
                source=product.source,
                price=product.price,
                currency=product.currency,
                product_url=product.product_url,
                rating=product.rating,
                review_count=product.review_count,
            )
            for product in products
        ]

        prices = [
            product.price
            for product in products
            if product.price is not None
        ]

        highest_price = max(prices)

        savings = (
            highest_price - best.price
            if best.price is not None
            else None
        )

        return GroupedProduct(
            title=best.title,
            price=best.price,
            currency=best.currency,
            rating=best.rating,
            review_count=best.review_count,
            image_url=best.image_url,
            product_url=best.product_url,
            source=best.source,
            lowest_price=best.lowest_price,
            average_price=best.average_price,
            deal_status=best.deal_status,
            offers=offers,
            offer_count=len(offers),
            savings=savings,
        )

    def group_products(
        self,
        products: list[Product],
    ) -> list[GroupedProduct]:
        """
        Group all products and return one grouped product
        per product identity.
        """

        groups = self.group(products)

        grouped_products: list[GroupedProduct] = []

        for product_group in groups.values():

            grouped_product = (
                self.create_grouped_product(
                    product_group
                )
            )

            if grouped_product is not None:
                grouped_products.append(
                    grouped_product
                )

        return grouped_products
