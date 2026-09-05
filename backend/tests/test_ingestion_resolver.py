from app.ingestion.resolver import ProductResolver


def test_resolver_selects_amazon_adapter():
    resolver = ProductResolver()

    adapter = resolver.resolve(
        "https://www.amazon.in/dp/B0ABC123"
    )

    assert adapter is not None
    assert adapter.__class__.__name__ == "AmazonAdapter"


def test_resolver_returns_none_for_unsupported_url():
    resolver = ProductResolver()

    adapter = resolver.resolve(
        "https://www.example.com/product/123"
    )

    assert adapter is None