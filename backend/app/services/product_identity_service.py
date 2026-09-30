import re


class ProductIdentityService:
    """
    Normalizes product titles so equivalent marketplace listings
    can be recognized as the same product.
    """

    def normalize_title(self, title: str) -> str:
        """
        Convert a product title into a normalized identity key.

        Example:
            "Samsung Galaxy A17 5g"
            "Samsung Galaxy A17 5G"

        Both become:

            "samsung galaxy a17 5g"
        """

        normalized = title.lower().strip()

        # Normalize common separators.
        normalized = re.sub(
            r"[-_/|]+",
            " ",
            normalized,
        )

        # Remove punctuation.
        normalized = re.sub(
            r"[^\w\s]",
            " ",
            normalized,
        )

        # Collapse repeated whitespace.
        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()

    def are_same_product(
        self,
        first_title: str,
        second_title: str,
    ) -> bool:
        """
        Determine whether two product titles represent
        the same normalized product.
        """

        return (
            self.normalize_title(first_title)
            == self.normalize_title(second_title)
        )