from app.schemas.offer import ProductOffer
from app.schemas.search import ProductSearchProduct


def test_product_search_product_supports_offers():
    product = ProductSearchProduct(
        title="Samsung Galaxy A17 5G",
        price=20499,
        currency="INR",
        rating=4.5,
        review_count=16000,
        product_url="https://example.com/a17",
        source="Samsung.com",
        offers=[
            ProductOffer(
                source="Samsung.com",
                price=20499,
                product_url=(
                    "https://example.com/samsung-a17"
                ),
            ),
            ProductOffer(
                source="Amazon.in",
                price=29999,
                product_url=(
                    "https://example.com/amazon-a17"
                ),
            ),
        ],
        offer_count=2,
        savings=9500,
    )

    assert product.title == "Samsung Galaxy A17 5G"
    assert product.price == 20499
    assert product.offer_count == 2
    assert len(product.offers) == 2
    assert product.savings == 9500


def test_product_search_product_defaults_to_no_offers():
    product = ProductSearchProduct(
        title="Samsung Galaxy A36 5G",
        price=28999,
        product_url="https://example.com/a36",
        source="Samsung.com",
    )

    assert product.offers == []
    assert product.offer_count == 0
    assert product.savings is None