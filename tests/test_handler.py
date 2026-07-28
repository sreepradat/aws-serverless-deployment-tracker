import json

from app.handler import lambda_handler


def test_health_response():
    response = lambda_handler({}, None)

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"

    body = json.loads(response["body"])

    assert body["status"] == "healthy"
    assert body["service"] == "deployment-tracker"