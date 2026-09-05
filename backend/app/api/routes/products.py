from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.ingestion.providers.factory import (
    create_serpapi_provider,
)
from app.ingestion.resolver import ProductResolver

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
    ProductSearchRequest,
    ProductSearchResponse,
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
    # Parse the natural-language query.
    parsed_query = query_parser.parse(
        request.query,
    )

    # Search products.
    products = await service.search(
        query=request.query,
        max_price=request.max_price,
        min_rating=request.min_rating,
        limit=request.limit,
    )

    # Return normalized products with
    # price intelligence included.
    return ProductSearchResponse(
        query=request.query,
        interpreted_query=parsed_query,
        products=[
            product.model_dump()
            for product in products
        ],
        total=len(products),
    )