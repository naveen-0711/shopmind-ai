import re

from app.schemas.query import ParsedSearchQuery


class QueryParser:
    def parse(self, query: str) -> ParsedSearchQuery:
        cleaned_query = query.strip()

        range_prices = self._extract_price_range(
            cleaned_query
        )

        if range_prices is not None:
            min_price, max_price = range_prices
        else:
            max_price = self._extract_max_price(
                cleaned_query
            )
            min_price = self._extract_min_price(
                cleaned_query
            )

        min_rating = self._extract_rating(
            cleaned_query
        )

        product_query = self._clean_product_query(
            cleaned_query
        )

        return ParsedSearchQuery(
            product_query=product_query,
            max_price=max_price,
            min_price=min_price,
            min_rating=min_rating,
        )

    def _parse_price(self, value: str) -> float:
        value = (
            value
            .replace(",", "")
            .strip()
            .lower()
        )

        # "1 lakh" / "1lakh"
        if re.fullmatch(
            r"\d+(?:\.\d+)?\s*lakh",
            value,
        ):
            number = re.sub(
                r"\s*lakh$",
                "",
                value,
            )
            return float(number) * 100_000

        # "1 lac" / "1lac"
        if re.fullmatch(
            r"\d+(?:\.\d+)?\s*lac",
            value,
        ):
            number = re.sub(
                r"\s*lac$",
                "",
                value,
            )
            return float(number) * 100_000

        # "30k"
        if value.endswith("k"):
            return float(value[:-1]) * 1_000

        # "1l"
        if value.endswith("l"):
            return float(value[:-1]) * 100_000

        return float(value)

    def _extract_price_range(
        self,
        query: str,
    ) -> tuple[float, float] | None:
        price_pattern = (
            r"[\d,.]+"
            r"(?:\s*(?:lakh|lac)|[kKlL])?"
        )

        patterns = [
            (
                r"between\s*₹?\s*("
                + price_pattern
                + r")\s*and\s*₹?\s*("
                + price_pattern
                + r")"
            ),
            (
                r"from\s*₹?\s*("
                + price_pattern
                + r")\s*to\s*₹?\s*("
                + price_pattern
                + r")"
            ),
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                min_price = self._parse_price(
                    match.group(1)
                )
                max_price = self._parse_price(
                    match.group(2)
                )

                return min_price, max_price

        return None

    def _extract_max_price(
        self,
        query: str,
    ) -> float | None:
        price_pattern = (
            r"[\d,.]+"
            r"(?:\s*(?:lakh|lac)|[kKlL])?"
        )

        patterns = [
            (
                r"(?:under|below|less than|upto|up to)"
                r"\s*₹?\s*("
                + price_pattern
                + r")"
            ),
            (
                r"₹?\s*("
                + price_pattern
                + r")"
                r"\s*(?:or less|and below)"
            ),
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                return self._parse_price(
                    match.group(1)
                )

        return None

    def _extract_min_price(
        self,
        query: str,
    ) -> float | None:
        price_pattern = (
            r"[\d,.]+"
            r"(?:\s*(?:lakh|lac)|[kKlL])?"
        )

        patterns = [
            (
                r"(?:above|over|more than)"
                r"\s*₹?\s*("
                + price_pattern
                + r")"
            ),
            (
                r"₹?\s*("
                + price_pattern
                + r")"
                r"\s*(?:or more|and above)"
            ),
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                return self._parse_price(
                    match.group(1)
                )

        return None

    def _extract_rating(
        self,
        query: str,
    ) -> float | None:
        patterns = [
            (
                r"(?:rating|rated)"
                r"\s*(?:of|above|over|at least)?"
                r"\s*([0-5](?:\.[0-9])?)\s*\+?"
            ),
            (
                r"([0-5](?:\.[0-9])?)"
                r"\s*\+?\s*(?:rating|rated)"
            ),
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                return float(match.group(1))

        return None

    def _clean_product_query(
        self,
        query: str,
    ) -> str:
        cleaned = query

        price_pattern = (
            r"[\d,.]+"
            r"(?:\s*(?:lakh|lac)|[kKlL])?"
        )

        patterns = [
            # Price ranges
            (
                r"between\s*₹?\s*"
                + price_pattern
                + r"\s*and\s*₹?\s*"
                + price_pattern
            ),
            (
                r"from\s*₹?\s*"
                + price_pattern
                + r"\s*to\s*₹?\s*"
                + price_pattern
            ),

            # Maximum price
            (
                r"(?:under|below|less than|upto|up to)"
                r"\s*₹?\s*"
                + price_pattern
            ),
            (
                r"₹?\s*"
                + price_pattern
                + r"\s*(?:or less|and below)"
            ),

            # Minimum price
            (
                r"(?:above|over|more than)"
                r"\s*₹?\s*"
                + price_pattern
            ),
            (
                r"₹?\s*"
                + price_pattern
                + r"\s*(?:or more|and above)"
            ),

            # Rating
            (
                r"(?:rating|rated)"
                r"\s*(?:of|above|over|at least)?"
                r"\s*[0-5](?:\.[0-9])?\s*\+?"
            ),
            (
                r"[0-5](?:\.[0-9])?"
                r"\s*\+?\s*(?:rating|rated)"
            ),
        ]

        for pattern in patterns:
            cleaned = re.sub(
                pattern,
                "",
                cleaned,
                flags=re.IGNORECASE,
            )

        cleaned = re.sub(
            r"\b(best|top|cheapest|budget)\b",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*\+\s*",
            " ",
            cleaned,
        )

        cleaned = re.sub(
            r"\b(with|having)\b",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        )

        return cleaned.strip()

