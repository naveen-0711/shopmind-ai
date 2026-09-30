from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.ingestion.providers.factory import (
    create_serpapi_provider,
)
from app.ingestion.resolver import ProductResolver

from app.intelligence.comparison_engine import (
    ComparisonEngine,
)
from app.intelligence.product_intelligence import (
    ProductIntelligenceService,
)
from app.intelligence.pros_cons_engine import (
    ProsConsEngine,
)

from app.repositories.price_observation_repository import (
    PriceObservationRepository,
)
from app.repositories.product_repository import (
    ProductRepository,
)

from app.schemas.product import (
    Product,
    ProductAnalyzeRequest,
)

from app.schemas.search import (
    ProductSearchProduct,
    ProductSearchRequest,
    ProductSearchResponse,
)

from app.services.offer_grouping_service import (
    OfferGroupingService,
)

from app.services.product_persistence_service import (
    ProductPersistenceService,
)

from app.services.product_search_service import (
    ProductSearchService,
)

from app.services.product_service import (
    ProductService,
)

from app.services.price_history_service import (
    PriceHistoryService,
)

from app.services.query_parser import QueryParser


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# ---------------------------------------------------------
# Product Analysis Dependency
# ---------------------------------------------------------

def get_product_service() -> ProductService:
    resolver = ProductResolver()

    return ProductService(
        resolver=resolver,
    )


# ---------------------------------------------------------
# Product Search Dependency
# ---------------------------------------------------------

def get_product_search_service(
    db: Session = Depends(get_db),
) -> ProductSearchService:

    # External product search provider
    provider = create_serpapi_provider()

    # Repositories
    product_repository = ProductRepository(
        session=db,
    )

    price_repository = PriceObservationRepository(
        session=db,
    )

    # Product persistence
    persistence_service = ProductPersistenceService(
        product_repository=product_repository,
        price_repository=price_repository,
    )

    # Price history
    price_history_service = PriceHistoryService(
        price_repository=price_repository,
    )

    # Complete search service
    return ProductSearchService(
        providers=[provider],
        persistence_service=persistence_service,
        price_history_service=price_history_service,
    )


# ---------------------------------------------------------
# Query Parser
# ---------------------------------------------------------

query_parser = QueryParser()


# ---------------------------------------------------------
# Offer Grouping
# ---------------------------------------------------------

offer_grouping_service = OfferGroupingService()


# ---------------------------------------------------------
# Product Intelligence
# ---------------------------------------------------------

product_intelligence_service = ProductIntelligenceService()


# ---------------------------------------------------------
# Comparison Engine
# ---------------------------------------------------------

comparison_engine = ComparisonEngine()


# ---------------------------------------------------------
# Pros & Cons Engine
# ---------------------------------------------------------

pros_cons_engine = ProsConsEngine()


# ---------------------------------------------------------
# Analyze Product
# ---------------------------------------------------------

@router.post(
    "/analyze",
    response_model=Product,
)
async def analyze_product(
    request: ProductAnalyzeRequest,
    service: ProductService = Depends(
        get_product_service,
    ),
):
    try:
        return await service.analyze_product(
            str(request.url),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail="Product extraction failed",
        ) from exc


# ---------------------------------------------------------
# Search Products
# ---------------------------------------------------------

@router.post(
    "/search",
    response_model=ProductSearchResponse,
)
async def search_products(
    request: ProductSearchRequest,
    service: ProductSearchService = Depends(
        get_product_search_service,
    ),
):
    # -----------------------------------------
    # 1. Parse natural-language query
    # -----------------------------------------

    parsed_query = query_parser.parse(
        request.query,
    )

    # -----------------------------------------
    # 2. Search products
    # -----------------------------------------

    products = await service.search(
        query=request.query,
        max_price=request.max_price,
        min_rating=request.min_rating,
        limit=request.limit,
    )

    # -----------------------------------------
    # 3. Group equivalent products
    # -----------------------------------------

    grouped_products = (
        offer_grouping_service.group_products(
            products,
        )
    )

    # -----------------------------------------
    # 4. Add recommendation + Pros & Cons
    # -----------------------------------------

    enriched_products: list[ProductSearchProduct] = []

    for product in grouped_products:

        # Recommendation intelligence
        explanation = product_intelligence_service.explain(
            rating=product.rating,
            review_count=product.review_count,
            current_price=product.price,
            reference_price=product.average_price,
            deal_status=product.deal_status,
        )

        # Create enriched product
        enriched_product = ProductSearchProduct(
            **product.model_dump(),
            recommendation_score=explanation["score"],
            recommendation_reasons=explanation["reasons"],
        )

        # Generate Pros & Cons
        pros_cons = pros_cons_engine.analyze(
            enriched_product,
        )

        # Attach Pros & Cons
        enriched_product.pros = pros_cons["pros"]
        enriched_product.cons = pros_cons["cons"]

        enriched_products.append(
            enriched_product,
        )

    # -----------------------------------------
    # 5. Compare all products
    # -----------------------------------------

    comparison = comparison_engine.compare(
        enriched_products,
    )

    # -----------------------------------------
    # 6. Convert comparison models to API data
    #
    # ComparisonEngine returns ProductSearchProduct
    # instances, while ProductComparisonSummary expects
    # ComparisonProduct models.
    #
    # model_dump() creates dictionaries that Pydantic
    # can validate into ComparisonProduct.
    # -----------------------------------------

    comparison_response = {
        key: (
            value.model_dump()
            if value is not None
            else None
        )
        for key, value in comparison.items()
    }

    # -----------------------------------------
    # 7. Return complete intelligent response
    # -----------------------------------------

    return ProductSearchResponse(
        query=request.query,
        interpreted_query=parsed_query,
        products=enriched_products,
        total=len(enriched_products),
        comparison=comparison_response,
    )