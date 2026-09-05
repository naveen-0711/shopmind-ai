from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


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


def test_product_analyze_api_end_to_end():

    with patch(
        "app.ingestion.adapters.amazon.ProductHttpClient"
    ) as mock_client:

        mock_client_instance = mock_client.return_value

        mock_client_instance.fetch = AsyncMock(
            return_value=AMAZON_HTML
        )

        with TestClient(app) as client:

            response = client.post(
                "/api/v1/products/analyze",
                json={
                    "url": "https://www.amazon.in/dp/B0TEST123"
                },
            )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Samsung Galaxy S24"
    assert data["price"] == 54999.0
    assert data["currency"] == "INR"
    assert data["rating"] == 4.6
    assert data["review_count"] == 2345
    assert data["image_url"] == (
        "https://example.com/s24.jpg"
    )
    assert data["product_url"] == (
        "https://www.amazon.in/dp/B0TEST123"
    )
    assert data["source"] == "amazon"

    mock_client_instance.fetch.assert_awaited_once_with(
        "https://www.amazon.in/dp/B0TEST123"
    )