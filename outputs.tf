output "api_url" {
  value = "${aws_api_gateway_stage.prod.invoke_url}/items"
}

# Prints the DynamoDB table name
output "dynamodb_table" {
  value = aws_dynamodb_table.items.name
}

# Prints the Lambda function name
output "lambda_function" {
  value = aws_lambda_function.api.function_name
}