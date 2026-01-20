// SNS for the purposes of notifying us when the remediation lambda has errors
resource "aws_sns_topic" "lambda_failure_alerts" {
  name = "cloudwatch-log-retention-lambda-failures"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.lambda_failure_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}
