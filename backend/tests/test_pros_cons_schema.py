from app.schemas.pros_cons import ProsConsResponse


def test_pros_cons_response_defaults_to_empty_lists():
    response = ProsConsResponse()

    assert response.pros == []
    assert response.cons == []


def test_pros_cons_response_accepts_pros_and_cons():
    response = ProsConsResponse(
        pros=[
            "Excellent 4.7/5 rating.",
            "Good deal.",
        ],
        cons=[
            "Limited review confidence.",
        ],
    )

    assert len(response.pros) == 2
    assert len(response.cons) == 1