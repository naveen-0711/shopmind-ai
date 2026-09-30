from fastapi import APIRouter

from app.intelligence.comparison_engine import ComparisonEngine
from app.schemas.comparison import (
    ProductComparisonResponse,
    ProductComparisonSummary,
)
from app.schemas.search import ProductSearchProduct


router = APIRouter(
    prefix="/products",
    tags=["comparison"],
)

comparison_engine = ComparisonEngine()


@router.post(
    "/compare",
    response_model=ProductComparisonResponse,
)
async def compare_products(
    query: str,
    products: list[ProductSearchProduct],
):
    comparison = comparison_engine.compare(products)

    return ProductComparisonResponse(
        query=query,
        summary=ProductComparisonSummary(
            **comparison,
        ),
        products=products,
    )