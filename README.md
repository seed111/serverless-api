# Serverless REST API on AWS

This project is a REST API built on AWS that can store and retrieve 
data. Everything was built using Terraform so it can be deployed 
from scratch with a few commands.


## How It Works

When a request hits the API, API Gateway receives it and sends it 
to a Lambda function. The Lambda function then reads or writes to 
a DynamoDB table depending on what the request is asking for.

Request → API Gateway → Lambda → DynamoDB → Response


## What the API Can Do

POST /items — creates a new item and saves it to the database

GET /items — returns everything stored in the database

GET /items/id — returns one specific item using its ID

DELETE /items/id — removes an item from the database


## Services Used

- Amazon API Gateway
- AWS Lambda (Python 3.12)
- Amazon DynamoDB
- AWS IAM
- Terraform


## Security

The Lambda function only has access to what it needs. It can read 
and write to DynamoDB but nothing else. The DynamoDB table name is 
not hardcoded in the code it gets passed in as an environment 
variable through Terraform.


## Testing the API

Create an item:

curl -X POST https://your-api-url/prod/items \
  -H "Content-Type: application/json" \
  -d '{"id": "1", "name": "Abraham"}'

Get all items:

curl https://your-api-url/prod/items

Get one item:

curl https://your-api-url/prod/items/1

Delete an item:

curl -X DELETE https://your-api-url/prod/items/1


## How to Deploy

Terraform and the AWS CLI need to be installed first.

1. Clone this repo
2. Run aws configure and enter your credentials
3. Create a terraform.tfvars file and add this:

project_name = "serverless-api"

4. Run these commands:

terraform init
terraform plan
terraform apply

5. Copy the api_url that prints in the terminal after apply 
   and use it to make requests


## Cost

This runs within the AWS Free Tier. At low usage the monthly 
cost is effectively zero.


## What Was Learned

This project helped with understanding how API Gateway, Lambda 
and DynamoDB work together. Writing the routing logic inside one 
Lambda function instead of having a separate function for each 
endpoint was a good way to keep things simple.

Writing the IAM policy manually made it easier to understand 
what permissions are actually needed and why least privilege 
matters in practice.