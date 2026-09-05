from unittest.mock import AsyncMock, patch

import pytest

from app.ingestion.adapters.amazon import AmazonAdapter


AMAZON_HTML = """
<html>
<body>

<h1 id="productTitle">
    Samsung Galaxy S24
</h1>

<span class="a-price-whole">54,999</span>

<span class="a-icon-alt">
    4.6 out of 5 stars
</span>

<span id="acrCustomerReviewText">
    2,345 ratings
</span>

<img
    id="landingImage"
    src="https://example.com/s24.jpg"
>

</body>
</html>
"""


@pytest.mark.anyio
async def test_amazon_adapter_fetches_and_extracts_product():

    with patch(
        "app.ingestion.adapters.amazon.ProductHttpClient"
    ) as mock_client, patch(
        "app.ingestion.adapters.amazon.ProductParser"
    ) as mock_parser:

        mock_client_instance = mock_client.return_value

        mock_client_instance.fetch = AsyncMock(
            return_value=AMAZON_HTML
        )

        mock_parser_instance = mock_parser.return_value

        mock_parser_instance.parse.return_value = {
            "title": "Samsung Galaxy S24",
            "price": 54999.0,
            "rating": 4.6,
            "review_count": 2345,
            "image_url": "https://example.com/s24.jpg",
        }

        # Create adapter AFTER applying the patches
        adapter = AmazonAdapter()

        result = await adapter.fetch_product(
            "https://www.amazon.in/dp/B0TEST123"
        )

    assert result["title"] == "Samsung Galaxy S24"
    assert result["price"] == 54999.0
    assert result["rating"] == 4.6
    assert result["review_count"] == 2345
    assert result["image_url"] == "https://example.com/s24.jpg"

    mock_client_instance.fetch.assert_awaited_once_with(
        "https://www.amazon.in/dp/B0TEST123"
    )

    mock_parser_instance.parse.assert_called_once_with(
        AMAZON_HTML
    )