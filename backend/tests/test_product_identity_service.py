from app.services.product_identity_service import (
    ProductIdentityService,
)


def test_normalize_title_ignores_case():
    service = ProductIdentityService()

    assert (
        service.normalize_title(
            "Samsung Galaxy A17 5G"
        )
        == "samsung galaxy a17 5g"
    )


def test_normalize_title_normalizes_separators():
    service = ProductIdentityService()

    assert (
        service.normalize_title(
            "Samsung-Galaxy_A17/5G"
        )
        == "samsung galaxy a17 5g"
    )


def test_normalize_title_removes_punctuation():
    service = ProductIdentityService()

    assert (
        service.normalize_title(
            "Samsung Galaxy A17 5G!"
        )
        == "samsung galaxy a17 5g"
    )


def test_normalize_title_collapses_whitespace():
    service = ProductIdentityService()

    assert (
        service.normalize_title(
            "Samsung   Galaxy    A17    5G"
        )
        == "samsung galaxy a17 5g"
    )


def test_same_product_with_different_case():
    service = ProductIdentityService()

    assert service.are_same_product(
        "Samsung Galaxy A17 5g",
        "Samsung Galaxy A17 5G",
    )


def test_same_product_with_different_separators():
    service = ProductIdentityService()

    assert service.are_same_product(
        "Samsung-Galaxy-A17-5G",
        "Samsung Galaxy A17 5G",
    )


def test_different_products_are_not_grouped():
    service = ProductIdentityService()

    assert not service.are_same_product(
        "Samsung Galaxy A17 5G",
        "Samsung Galaxy A36 5G",
    )