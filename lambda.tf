data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "log_retention_enforcer" {
  function_name = "cloudwatch-log-retention-enforcer"
  role          = aws_iam_role.lambda_role.arn
  handler       = "retention_enforcer.lambda_handler"
  runtime       = "python3.14"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout     = 300
  memory_size = 128
}
