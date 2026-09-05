import httpx


class ProductHttpClient:
    """
    HTTP client used to fetch product pages.
    """

    def __init__(self) -> None:
        self.timeout = 15.0

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    async def fetch(self, url: str) -> str:
        """
        Fetch the HTML content of a product page.
        """

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers,
                follow_redirects=True,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

                return response.text

        except Exception as exc:
            raise RuntimeError(
                "Failed to fetch product page"
            ) from exc