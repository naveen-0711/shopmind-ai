from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.ingestion.http_client import ProductHttpClient


@pytest.mark.anyio
async def test_http_client_fetches_page():
    client = ProductHttpClient()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html>Product page</html>"

    with patch(
        "app.ingestion.http_client.httpx.AsyncClient"
    ) as mock_client:

        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.get.return_value = mock_response

        html = await client.fetch(
            "https://www.amazon.in/dp/B0ABC123"
        )

    assert html == "<html>Product page</html>"

    mock_instance.get.assert_awaited_once()

    
@pytest.mark.anyio
async def test_http_client_raises_for_failed_request():
    client = ProductHttpClient()

    with patch(
        "app.ingestion.http_client.httpx.AsyncClient"
    ) as mock_client:

        mock_instance = mock_client.return_value.__aenter__.return_value

        mock_instance.get.side_effect = Exception(
            "Connection failed"
        )

        with pytest.raises(RuntimeError, match="Failed to fetch product page"):
            await client.fetch(
                "https://www.amazon.in/dp/B0ABC123"
            )