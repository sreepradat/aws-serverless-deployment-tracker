import json


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


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

    return build_response(
        404,
        {
            "message": "route not found",
        },
    )