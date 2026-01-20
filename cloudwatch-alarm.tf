// alarm to be generated if the remediation lambda fails
resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "cloudwatch-log-retention-lambda-errors"
  alarm_description   = "Alarm when CloudWatch log retention Lambda reports errors"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"

  dimensions = {
    FunctionName = aws_lambda_function.log_retention_enforcer.function_name
  }

  alarm_actions = [
    aws_sns_topic.lambda_failure_alerts.arn
  ]

  treat_missing_data = "notBreaching"
}
