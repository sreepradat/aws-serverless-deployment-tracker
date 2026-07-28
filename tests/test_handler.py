import json
from unittest.mock import patch

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
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
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


@patch("app.handler.save_deployment")
def test_create_deployment_success(mock_save_deployment):
    event = {
        "rawPath": "/deployments",
        "requestContext": {
            "http": {
                "method": "POST",
            },
        },
        "body": json.dumps(
            {
                "application": "payment-api",
                "version": "1.0.0",
                "environment": "dev",
                "status": "success",
            }
        ),
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 201
    assert body["application"] == "payment-api"
    assert body["version"] == "1.0.0"
    assert body["environment"] == "dev"
    assert body["status"] == "success"
    assert "deploymentId" in body
    assert "createdAt" in body

    mock_save_deployment.assert_called_once_with(body)


@patch("app.handler.save_deployment")
def test_create_deployment_missing_fields(mock_save_deployment):
    event = {
        "rawPath": "/deployments",
        "requestContext": {
            "http": {
                "method": "POST",
            },
        },
        "body": json.dumps(
            {
                "application": "payment-api",
            }
        ),
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["message"] == "missing required fields"
    assert body["missingFields"] == [
        "version",
        "environment",
        "status",
    ]

    mock_save_deployment.assert_not_called()


@patch("app.handler.save_deployment")
def test_create_deployment_invalid_json(mock_save_deployment):
    event = {
        "rawPath": "/deployments",
        "requestContext": {
            "http": {
                "method": "POST",
            },
        },
        "body": "{invalid-json}",
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["message"] == "invalid JSON body"

    mock_save_deployment.assert_not_called()