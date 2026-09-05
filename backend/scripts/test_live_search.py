
import asyncio

from app.ingestion.providers.factory import (
    create_serpapi_provider,
)
from app.services.product_search_service import (
    ProductSearchService,
)


async def main():
    service = ProductSearchService(
        providers=[
            create_serpapi_provider()
        ]
    )

    results = await service.search(
        query=(
            "best Samsung phone under 30000 "
            "with rating 4.5+"
        ),
        limit=10,
    )

    print()
    print("=" * 70)
    print("LIVE SEARCH RESULTS")
    print("=" * 70)

    print(f"Results found: {len(results)}")
    print()

    for index, product in enumerate(
        results,
        start=1,
    ):
        print(f"{index}. {product.title}")
        print(f"   Price: ₹{product.price}")
        print(f"   Rating: {product.rating}")
        print(f"   Reviews: {product.review_count}")
        print(f"   Source: {product.source}")
        print(f"   URL: {product.product_url}")
        print()


if __name__ == "__main__":
    asyncio.run(main())

