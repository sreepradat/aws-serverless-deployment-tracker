from unittest.mock import MagicMock

import pytest

from app.storage import get_deployments_table, save_deployment


def test_save_deployment_writes_item():
    mock_table = MagicMock()

    deployment = {
        "deploymentId": "deployment-123",
        "application": "payment-api",
        "version": "1.0.0",
        "environment": "dev",
        "status": "success",
        "createdAt": "2026-07-28T09:16:13+00:00",
    }

    result = save_deployment(
        deployment,
        table=mock_table,
    )

    mock_table.put_item.assert_called_once_with(
        Item=deployment,
    )

    assert result == deployment


def test_get_deployments_table_uses_given_table_name():
    mock_resource = MagicMock()
    mock_table = MagicMock()

    mock_resource.Table.return_value = mock_table

    result = get_deployments_table(
        table_name="deployment-tracker-dev",
        dynamodb_resource=mock_resource,
    )

    mock_resource.Table.assert_called_once_with(
        "deployment-tracker-dev"
    )

    assert result == mock_table


def test_get_deployments_table_requires_table_name(monkeypatch):
    monkeypatch.delenv(
        "DEPLOYMENTS_TABLE",
        raising=False,
    )

    with pytest.raises(
        ValueError,
        match="DEPLOYMENTS_TABLE environment variable is required",
    ):
        get_deployments_table()