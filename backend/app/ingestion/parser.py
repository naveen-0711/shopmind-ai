import re
from typing import Any

from bs4 import BeautifulSoup


class ProductParser:
    """
    Parses product information from HTML.
    """

    def parse(self, html: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")

        return {
            "title": self._extract_title(soup),
            "price": self._extract_price(soup),
            "rating": self._extract_rating(soup),
            "review_count": self._extract_review_count(soup),
            "image_url": self._extract_image_url(soup),
        }

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        element = soup.select_one("#productTitle")

        if not element:
            return None

        title = element.get_text(strip=True)

        return title or None

    def _extract_price(
        self,
        soup: BeautifulSoup,
    ) -> float | None:
        element = soup.select_one(".a-price-whole")

        if not element:
            return None

        text = element.get_text(strip=True)

        text = text.replace(",", "").replace("₹", "").strip()

        try:
            return float(text)
        except ValueError:
            return None

    def _extract_rating(
        self,
        soup: BeautifulSoup,
    ) -> float | None:
        element = soup.select_one(".a-icon-alt")

        if not element:
            return None

        text = element.get_text(strip=True)

        match = re.search(
            r"(\d+(?:\.\d+)?)\s+out of 5",
            text,
        )

        if not match:
            return None

        return float(match.group(1))

    def _extract_review_count(
        self,
        soup: BeautifulSoup,
    ) -> int | None:
        element = soup.select_one("#acrCustomerReviewText")

        if not element:
            return None

        text = element.get_text(strip=True)

        match = re.search(
            r"([\d,]+)",
            text,
        )

        if not match:
            return None

        return int(match.group(1).replace(",", ""))

    def _extract_image_url(
        self,
        soup: BeautifulSoup,
    ) -> str | None:
        element = soup.select_one("#landingImage")

        if not element:
            return None

        return element.get("src")