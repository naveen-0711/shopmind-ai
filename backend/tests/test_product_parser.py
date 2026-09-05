from app.ingestion.parser import ProductParser


SAMPLE_HTML = """
<html>
<head>
    <title>Test Product</title>
</head>

<body>
    <h1 id="productTitle">
        Samsung Galaxy Phone
    </h1>

    <span class="a-price-whole">24,999</span>

    <span class="a-icon-alt">
        4.5 out of 5 stars
    </span>

    <span id="acrCustomerReviewText">
        1,234 ratings
    </span>

    <img id="landingImage"
         src="https://example.com/phone.jpg">
</body>
</html>
"""


def test_parser_extracts_product_title():
    parser = ProductParser()

    result = parser.parse(SAMPLE_HTML)

    assert result["title"] == "Samsung Galaxy Phone"


def test_parser_extracts_price():
    parser = ProductParser()

    result = parser.parse(SAMPLE_HTML)

    assert result["price"] == 24999.0


def test_parser_extracts_rating():
    parser = ProductParser()

    result = parser.parse(SAMPLE_HTML)

    assert result["rating"] == 4.5


def test_parser_extracts_review_count():
    parser = ProductParser()

    result = parser.parse(SAMPLE_HTML)

    assert result["review_count"] == 1234


def test_parser_extracts_image_url():
    parser = ProductParser()

    result = parser.parse(SAMPLE_HTML)

    assert result["image_url"] == "https://example.com/phone.jpg"


def test_parser_handles_missing_fields():
    parser = ProductParser()

    result = parser.parse(
        "<html><body></body></html>"
    )

    assert result["title"] is None
    assert result["price"] is None
    assert result["rating"] is None
    assert result["review_count"] is None
    assert result["image_url"] is None