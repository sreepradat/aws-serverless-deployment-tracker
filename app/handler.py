import json


def lambda_handler(event, context):
    body = {
        "status": "healthy",
        "service": "deployment-tracker",
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }