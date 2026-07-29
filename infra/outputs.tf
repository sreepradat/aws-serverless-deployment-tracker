output "deployments_table_name" {
  description = "Name of the DynamoDB deployments table"
  value       = aws_dynamodb_table.deployments.name
}

output "deployments_table_arn" {
  description = "ARN of the DynamoDB deployments table"
  value       = aws_dynamodb_table.deployments.arn
}