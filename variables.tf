variable "alert_email" {
  description = "Email address to receive Lambda failure alerts"
  type        = string
  default     = "aws-landing-zones@itgix.com"
}

variable "python_runtime_version" {
  description = "Python Runtime Version for the Lambda"
  type        = string
  default     = "python3.14"
}
