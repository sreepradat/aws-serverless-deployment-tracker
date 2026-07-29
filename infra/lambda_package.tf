data "archive_file" "deployment_tracker" {
  type        = "zip"
  output_path = "${path.module}/deployment-tracker.zip"

  source {
    content  = file("${path.module}/../app/__init__.py")
    filename = "app/__init__.py"
  }

  source {
    content  = file("${path.module}/../app/handler.py")
    filename = "app/handler.py"
  }

  source {
    content  = file("${path.module}/../app/storage.py")
    filename = "app/storage.py"
  }
}