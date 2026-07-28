import json
from datetime import UTC, datetime
from uuid import uuid4

from app.storage import save_deployment


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def parse_request_body(event):
    raw_body = event.get("body")

    if not raw_body:
        return None

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return None


def lambda_handler(event, context):
    request_context = event.get("requestContext", {})
    http_context = request_context.get("http", {})

    method = http_context.get("method", "GET")
    path = event.get("rawPath", "/health")

    if method == "GET" and path == "/health":
        return build_response(
            200,
            {
                "status": "healthy",
                "service": "deployment-tracker",
            },
        )

    if method == "POST" and path == "/deployments":
        request_body = parse_request_body(event)

        if request_body is None:
            return build_response(
                400,
                {
                    "message": "invalid JSON body",
                },
            )

        required_fields = [
            "application",
            "version",
            "environment",
            "status",
        ]

        missing_fields = [
            field
            for field in required_fields
            if not request_body.get(field)
        ]

        if missing_fields:
            return build_response(
                400,
                {
                    "message": "missing required fields",
                    "missingFields": missing_fields,
                },
            )

        deployment = {
            "deploymentId": str(uuid4()),
            "application": request_body["application"],
            "version": request_body["version"],
            "environment": request_body["environment"],
            "status": request_body["status"],
            "createdAt": datetime.now(UTC).isoformat(),
        }

        save_deployment(deployment)

        return build_response(201, deployment)

    return build_response(
        404,
        {
            "message": "route not found",
        },
    )