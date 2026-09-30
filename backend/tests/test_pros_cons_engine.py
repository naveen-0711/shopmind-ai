from app.intelligence.pros_cons_engine import ProsConsEngine
from app.schemas.search import ProductSearchProduct


def make_product(
    *,
    title="Test Product",
    price=20000,
    rating=4.5,
    review_count=1000,
    lowest_price=18000,
    average_price=22000,
    deal_status="Good Deal",
    recommendation_score=85,
):
    return ProductSearchProduct(
        title=title,
        price=price,
        currency="INR",
        rating=rating,
        review_count=review_count,
        image_url=None,
        product_url="https://example.com/product",
        source="Example Store",
        lowest_price=lowest_price,
        average_price=average_price,
        deal_status=deal_status,
        offers=[],
        offer_count=1,
        savings=2000,
        recommendation_score=recommendation_score,
        recommendation_reasons=[],
    )


class TestProsConsEngine:
    def setup_method(self):
        self.engine = ProsConsEngine()

    # ---------------------------------------------------------
    # Strong product
    # ---------------------------------------------------------

    def test_high_rating_should_be_a_pro(self):
        product = make_product(rating=4.7)

        result = self.engine.analyze(product)

        assert any(
            "rating" in pro.lower()
            for pro in result["pros"]
        )

    def test_high_review_count_should_be_a_pro(self):
        product = make_product(review_count=5000)

        result = self.engine.analyze(product)

        assert any(
            "review" in pro.lower()
            for pro in result["pros"]
        )

    def test_good_deal_should_be_a_pro(self):
        product = make_product(
            deal_status="Good Deal"
        )

        result = self.engine.analyze(product)

        assert any(
            "deal" in pro.lower()
            for pro in result["pros"]
        )

    def test_great_deal_should_be_a_pro(self):
        product = make_product(
            deal_status="Great Deal"
        )

        result = self.engine.analyze(product)

        assert any(
            "deal" in pro.lower()
            for pro in result["pros"]
        )

    def test_price_below_average_should_be_a_pro(self):
        product = make_product(
            price=18000,
            average_price=22000,
        )

        result = self.engine.analyze(product)

        assert any(
            "price" in pro.lower()
            or "average" in pro.lower()
            for pro in result["pros"]
        )

    def test_high_recommendation_score_should_be_a_pro(self):
        product = make_product(
            recommendation_score=90
        )

        result = self.engine.analyze(product)

        assert any(
            "score" in pro.lower()
            or "recommend" in pro.lower()
            for pro in result["pros"]
        )

    # ---------------------------------------------------------
    # Weak product
    # ---------------------------------------------------------

    def test_low_rating_should_be_a_con(self):
        product = make_product(rating=3.2)

        result = self.engine.analyze(product)

        assert any(
            "rating" in con.lower()
            for con in result["cons"]
        )

    def test_low_review_count_should_be_a_con(self):
        product = make_product(review_count=10)

        result = self.engine.analyze(product)

        assert any(
            "review" in con.lower()
            for con in result["cons"]
        )

    def test_expensive_product_should_be_a_con(self):
        product = make_product(
            price=30000,
            average_price=22000,
        )

        result = self.engine.analyze(product)

        assert any(
            "price" in con.lower()
            or "expensive" in con.lower()
            or "average" in con.lower()
            for con in result["cons"]
        )

    def test_fair_price_should_not_be_presented_as_strong_deal(self):
        product = make_product(
            deal_status="Fair Price"
        )

        result = self.engine.analyze(product)

        assert not any(
            "great deal" in pro.lower()
            for pro in result["pros"]
        )

    def test_expensive_status_should_be_a_con(self):
        product = make_product(
            deal_status="Expensive"
        )

        result = self.engine.analyze(product)

        assert any(
            "expensive" in con.lower()
            or "price" in con.lower()
            for con in result["cons"]
        )

    def test_low_recommendation_score_should_be_a_con(self):
        product = make_product(
            recommendation_score=40
        )

        result = self.engine.analyze(product)

        assert any(
            "score" in con.lower()
            or "recommend" in con.lower()
            for con in result["cons"]
        )

    # ---------------------------------------------------------
    # Missing data
    # ---------------------------------------------------------

    def test_missing_rating_should_not_crash(self):
        product = make_product(
            rating=None
        )

        result = self.engine.analyze(product)

        assert "pros" in result
        assert "cons" in result

    def test_missing_price_should_not_crash(self):
        product = make_product(
            price=None
        )

        result = self.engine.analyze(product)

        assert "pros" in result
        assert "cons" in result

    def test_missing_review_count_should_not_crash(self):
        product = make_product(
            review_count=None
        )

        result = self.engine.analyze(product)

        assert "pros" in result
        assert "cons" in result

    def test_result_should_contain_lists(self):
        product = make_product()

        result = self.engine.analyze(product)

        assert isinstance(result["pros"], list)
        assert isinstance(result["cons"], list)