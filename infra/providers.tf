provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "aws-serverless-deployment-tracker"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}