The Terraform module is used by the ITGix AWS Landing Zone - https://itgix.com/itgix-landing-zone/

# AWS CloudWatch Log Retention Terraform Module

This module deploys a Lambda function that automatically sets retention policies on CloudWatch Log Groups, with EventBridge triggers and SNS alerting on failures.

Part of the [ITGix AWS Landing Zone](https://itgix.com/itgix-landing-zone/).

## Resources Created

- Lambda function for setting log group retention
- EventBridge rule to trigger Lambda on new log group creation
- IAM role and policy for Lambda execution
- SNS topic for Lambda failure alerts
- CloudWatch alarm for Lambda errors

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `alert_email` | Email address to receive Lambda failure alerts | `string` | `"aws-landing-zones@itgix.com"` | no |

## Usage Example

```hcl
module "cw_log_retention" {
  source = "path/to/tf-module-aws-cw-log-retention"

  alert_email = "alerts@example.com"
}
```
