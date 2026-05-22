# Serverless REST API on AWS

> A fully serverless REST API built on AWS that can store and retrieve data. All infrastructure is defined in Terraform and deployable from scratch in under two minutes with a single command.

[![AWS](https://img.shields.io/badge/Cloud-AWS-orange?style=flat-square)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?style=flat-square)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Runtime-Python%203.12-blue?style=flat-square)](https://www.python.org/)
[![Serverless](https://img.shields.io/badge/Architecture-Serverless-green?style=flat-square)](https://aws.amazon.com/serverless/)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [How It Works](#how-it-works)
3. [API Endpoints](#api-endpoints)
4. [Services Used](#services-used)
5. [IAM Roles and Privileges](#iam-roles-and-privileges)
6. [Security Practices](#security-practices)
7. [Testing the API](#testing-the-api)
8. [Deploy from Scratch](#deploy-from-scratch)
9. [Destroy Infrastructure](#destroy-infrastructure)
10. [Cost](#cost)
11. [What Was Learned](#what-was-learned)

---

This project was built to understand how API Gateway, Lambda and DynamoDB work together as a complete serverless backend. It is the foundation of what most AWS backend systems are built on including what Neulabs uses.
What it specifically proves:
It shows you understand how to build a REST API without managing any servers. No EC2, no load balancer, no container — just API Gateway receiving requests, Lambda processing them and DynamoDB storing the data. The whole thing scales automatically and costs nothing at low usage.

## Architecture Overview

```
Client Request
      ↓
Amazon API Gateway (receives and routes the request)
      ↓
AWS Lambda (reads the route and runs the right logic)
      ↓
Amazon DynamoDB (stores or retrieves the data)
      ↓
Response back to client
```

---

## How It Works

When a request hits the API, Amazon API Gateway receives it and forwards it to a single Lambda function. API Gateway acts as the front door of the system. It handles incoming HTTP requests, validates the route and method, and passes the full request details to Lambda.

The Lambda function is the brain of the API. Instead of having a separate Lambda function for each endpoint, a single function handles all four routes. It reads the HTTP method and the path from the request, decides what operation to perform, and either reads from or writes to DynamoDB depending on what the request is asking for.

Amazon DynamoDB stores all the data. It is a fully managed NoSQL database that requires no server management. It scales automatically and costs nothing at low usage. Each item is stored with a unique ID that can be used to retrieve or delete it later.

AWS IAM controls what Lambda is allowed to do. The function has a dedicated role that gives it only the permissions it needs to interact with DynamoDB and write logs to CloudWatch.

Terraform manages all of this infrastructure as code. The API Gateway, Lambda function, DynamoDB table and IAM role are all defined in Terraform files. The entire system can be deployed from scratch or destroyed with one command.

---

## API Endpoints

| Method | Endpoint | What It Does |
|---|---|---|
| POST | /items | Creates a new item and saves it to DynamoDB |
| GET | /items | Returns all items stored in the database |
| GET | /items/{id} | Returns one specific item using its ID |
| DELETE | /items/{id} | Removes an item from the database |

All four endpoints are handled by a single Lambda function. The function reads the HTTP method and path from the incoming request and routes the logic internally. This keeps the architecture simple and reduces the number of Lambda functions to manage.

---

## Services Used

**Amazon API Gateway** — receives incoming HTTP requests, routes them to Lambda and returns the response to the client. It acts as the public entry point of the API and handles all the HTTP layer concerns.

**AWS Lambda Python 3.12** — the compute layer of the API. It contains all the routing logic and handles all four endpoints. It reads from and writes to DynamoDB depending on the request and returns the appropriate response.

**Amazon DynamoDB** — the database layer. It stores all items with a unique ID as the partition key. Pay-per-request billing means there is no minimum cost and no capacity planning needed.

**AWS IAM** — controls permissions across the system. Lambda has a dedicated role that gives it only the access it needs to DynamoDB and CloudWatch. Nothing more is granted.

**Terraform** — defines and deploys all the infrastructure as code. The entire system is deployable from scratch with terraform apply and destroyable with terraform destroy.

---

## IAM Roles and Privileges

One IAM role was created for this system. It has only the permissions the Lambda function needs and nothing more.

### Lambda Execution Role

This role is used by the Lambda function when it runs. It needs four permissions on DynamoDB scoped to the specific table only.

`dynamodb:PutItem` — allows Lambda to create new items when a POST request comes in.

`dynamodb:GetItem` — allows Lambda to retrieve a single item by ID when a GET request with an ID comes in.

`dynamodb:Scan` — allows Lambda to retrieve all items when a GET request with no ID comes in.

`dynamodb:DeleteItem` — allows Lambda to remove an item when a DELETE request comes in.

The role also needs `logs:CreateLogGroup`, `logs:CreateLogStream` and `logs:PutLogEvents` so Lambda can write execution logs to CloudWatch for monitoring and debugging.

### What Was Not Granted

Lambda cannot update existing items, cannot access any other DynamoDB table, cannot interact with S3, EC2 or any other AWS service. The role is scoped as tightly as possible to what the API actually needs.

---

## Security Practices

The DynamoDB table name is never hardcoded in the Lambda function. It is passed in as an environment variable through Terraform so the same code can be reused across different environments without any changes. AWS credentials are never stored in the code. The Lambda function uses its IAM role to authenticate with AWS automatically at runtime.

---

## Testing the API

**Create an item**

```bash
curl -X POST https://your-api-url/prod/items \
  -H "Content-Type: application/json" \
  -d '{"id": "1", "name": "Abraham"}'
```

**Get all items**

```bash
curl https://your-api-url/prod/items
```

**Get one item**

```bash
curl https://your-api-url/prod/items/1
```

**Delete an item**

```bash
curl -X DELETE https://your-api-url/prod/items/1
```

Replace `your-api-url` with the `api_url` value that Terraform prints after deployment.

---

## Deploy from Scratch

**Prerequisites**

- AWS CLI configured
- Terraform installed

**Steps**

```bash
# 1. Clone this repo
git clone https://github.com/seed111/serverless-api.git
cd serverless-api

# 2. Configure AWS credentials
aws configure

# 3. Create a terraform.tfvars file
echo 'project_name = "serverless-api"' > terraform.tfvars

# 4. Deploy
terraform init
terraform plan
terraform apply
```

Copy the `api_url` that prints in the terminal after apply and use it to make requests.

---

## Destroy Infrastructure

```bash
terraform destroy
```

This removes all AWS resources created by Terraform including the API Gateway, Lambda function, DynamoDB table and IAM role.

---

## Cost

Runs within the AWS Free Tier. API Gateway, Lambda and DynamoDB all have generous free tiers that cover this project at low usage. The monthly cost at low traffic is effectively zero.

---

## What Was Learned

Handling all four endpoints inside a single Lambda function instead of creating a separate function for each one was a deliberate choice. It keeps the architecture simple, reduces cold start overhead and makes the code easier to maintain. In a production system with many endpoints separating functions by domain would make more sense.

Writing the IAM policy manually made it easier to understand what permissions are actually needed and why least privilege matters in practice. Scoping the DynamoDB permissions to the specific table ARN instead of using a wildcard ensures Lambda cannot accidentally access or modify any other table in the account.

---

## Author

**Fayemi Abraham** — Cloud & DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-seed111-black?style=flat-square&logo=github)](https://github.com/seed111)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Fayemi%20Abraham-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/abraham-fayemi-0032382a0)
