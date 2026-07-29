resource "aws_dynamodb_table" "deployments" {
  name         = "deployment-tracker-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "deploymentId"

  attribute {
    name = "deploymentId"
    type = "S"
  }

  tags = {
    Name = "deployment-tracker-${var.environment}"
  }
}