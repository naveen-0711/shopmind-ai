from unittest.mock import AsyncMock, patch

import pytest

from app.ingestion.adapters.amazon import AmazonAdapter
from app.ingestion.resolver import ProductResolver
from app.services.product_service import ProductService


@pytest.mark.anyio
async def test_product_service_analyzes_amazon_product():

    raw_product = {
        "title": "Samsung Galaxy S24",
        "price": 54999.0,
        "rating": 4.6,
        "review_count": 2345,
        "image_url": "https://example.com/s24.jpg",
    }

    with patch(
        "app.ingestion.adapters.amazon.ProductHttpClient"
    ) as mock_client:

        mock_client_instance = mock_client.return_value

        mock_client_instance.fetch = AsyncMock(
            return_value="<html>Amazon product page</html>"
        )

        with patch(
            "app.ingestion.adapters.amazon.ProductParser"
        ) as mock_parser:

            mock_parser_instance = mock_parser.return_value

            mock_parser_instance.parse.return_value = raw_product

            resolver = ProductResolver()
            service = ProductService(resolver)

            result = await service.analyze_product(
                "https://www.amazon.in/dp/B0TEST123"
            )

    assert result.title == "Samsung Galaxy S24"
    assert result.price == 54999.0
    assert result.rating == 4.6
    assert result.review_count == 2345
    assert result.image_url == "https://example.com/s24.jpg"
    assert result.product_url == (
        "https://www.amazon.in/dp/B0TEST123"
    )
    assert result.source == "amazon"