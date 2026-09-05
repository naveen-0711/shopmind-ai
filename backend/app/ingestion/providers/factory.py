
from app.core.config import settings
from app.ingestion.providers.serpapi_search import (
    SerpApiSearchProvider,
)


def create_serpapi_provider() -> SerpApiSearchProvider:
    return SerpApiSearchProvider(
        api_key=settings.serpapi_api_key,
    )
