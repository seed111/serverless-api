variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Used to name all resources"
  type        = string
  default     = "serverless-api"
}