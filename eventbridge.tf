resource "aws_cloudwatch_event_rule" "weekly_rule" {
  name                = "weekly-cloudwatch-log-retention-check"
  description         = "Runs weekly to enforce CloudWatch Logs retention policy"
  schedule_expression = "rate(7 days)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekly_rule.name
  target_id = "log-retention-lambda"
  arn       = aws_lambda_function.log_retention_enforcer.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.log_retention_enforcer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_rule.arn
}
