import os

import boto3


def get_deployments_table(table_name=None, dynamodb_resource=None):
    resolved_table_name = table_name or os.environ.get("DEPLOYMENTS_TABLE")

    if not resolved_table_name:
        raise ValueError("DEPLOYMENTS_TABLE environment variable is required")

    resource = dynamodb_resource or boto3.resource("dynamodb")

    return resource.Table(resolved_table_name)


def save_deployment(deployment, table=None):
    deployment_table = table or get_deployments_table()

    deployment_table.put_item(
        Item=deployment,
    )

    return deployment