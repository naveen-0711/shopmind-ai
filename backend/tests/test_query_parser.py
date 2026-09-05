
from app.schemas.query import ParsedSearchQuery


def test_parsed_query_accepts_product_query():
    result = ParsedSearchQuery(
        product_query="Samsung phone",
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price is None
    assert result.min_price is None
    assert result.min_rating is None


def test_parsed_query_accepts_max_price():
    result = ParsedSearchQuery(
        product_query="Samsung phone",
        max_price=30000,
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 30000


def test_parsed_query_accepts_min_price():
    result = ParsedSearchQuery(
        product_query="Samsung phone",
        min_price=20000,
    )

    assert result.min_price == 20000


def test_parsed_query_accepts_min_rating():
    result = ParsedSearchQuery(
        product_query="Samsung phone",
        min_rating=4.5,
    )

    assert result.min_rating == 4.5


def test_parsed_query_rejects_invalid_rating():
    try:
        ParsedSearchQuery(
            product_query="Samsung phone",
            min_rating=6,
        )
        assert False
    except ValueError:
        assert True


from app.services.query_parser import QueryParser


def test_parser_extracts_max_price():
    parser = QueryParser()

    result = parser.parse(
        "best Samsung phone under ₹30,000"
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 30000


def test_parser_extracts_min_price():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone above ₹20,000"
    )

    assert result.product_query == "Samsung phone"
    assert result.min_price == 20000



def test_parser_extracts_rating():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone with rating 4.5+"
    )

    assert result.product_query == "Samsung phone"
    assert result.min_rating == 4.5


def test_parser_extracts_multiple_constraints():
    parser = QueryParser()

    result = parser.parse(
        "best Samsung phone under ₹30,000 "
        "with rating 4.5+"
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 30000
    assert result.min_rating == 4.5



def test_parser_handles_plain_product_query():
    parser = QueryParser()

    result = parser.parse(
        "Samsung Galaxy phone"
    )

    assert result.product_query == "Samsung Galaxy phone"
    assert result.max_price is None
    assert result.min_price is None
    assert result.min_rating is None


def test_parser_extracts_k_price():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone under ₹30k"
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 30000


def test_parser_extracts_k_price_without_currency():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone under 30K"
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 30000


def test_parser_extracts_lakh_price():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone under ₹1.5L"
    )

    assert result.product_query == "Samsung phone"
    assert result.max_price == 150000


def test_parser_extracts_price_range():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone between ₹20,000 and ₹30,000"
    )

    assert result.product_query == "Samsung phone"
    assert result.min_price == 20000
    assert result.max_price == 30000


def test_parser_extracts_k_price_range():
    parser = QueryParser()

    result = parser.parse(
        "Samsung phone from 20k to 30k"
    )

    assert result.product_query == "Samsung phone"
    assert result.min_price == 20000
    assert result.max_price == 30000


def test_parser_extracts_lakh_price_range():
    parser = QueryParser()

    result = parser.parse(
        "laptop between 50k and 1 lakh"
    )

    assert result.product_query == "laptop"
    assert result.min_price == 50000
    assert result.max_price == 100000
