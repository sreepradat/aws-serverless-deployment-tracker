import json

from app.handler import lambda_handler


def test_health_response():
    event = {
        "rawPath": "/health",
        "requestContext": {
            "http": {
                "method": "GET",
            },
        },
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"

    body = json.loads(response["body"])

    assert body["status"] == "healthy"
    assert body["service"] == "deployment-tracker"


def test_unknown_route_returns_not_found():
    event = {
        "rawPath": "/unknown",
        "requestContext": {
            "http": {
                "method": "GET",
            },
        },
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 404
    assert body["message"] == "route not found"