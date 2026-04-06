# Serverless Todo API
A serverless REST API built on AWS with no servers to manage. Create, read, update, and delete tasks via HTTP — runs on Lambda, API Gateway, and DynamoDB, entirely within free tier.

## Architecture
Client → API Gateway → Lambda (Python) → DynamoDB

| Service | Role | Cost |
|---|---|---|
| AWS Lambda | Runs the application code | Free (1M requests/month) |
| API Gateway | Exposes HTTP endpoints | Free (1M calls/month) |
| DynamoDB | Stores task data | Free (25GB forever) |

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | /todos | List all tasks |
| POST | /todos | Create a new task |
| PUT | /todos/{id} | Mark a task done/undone |
| DELETE | /todos/{id} | Delete a task |

## Example Usage

Create a task:
curl -X POST https://zyao7mvczc.execute-api.us-east-1.amazonaws.com/prod/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Build something cool"}'

Response:
{
  "id": "f093b366-4d78-4497-af2d-37e5138b4a4a",
  "task": "Build something cool",
  "done": false,
  "created_at": "2026-03-12T18:34:07"
}

List all tasks:
curl https://zyao7mvczc.execute-api.us-east-1.amazonaws.com/prod/todos

Mark a task done:
curl -X PUT https://zyao7mvczc.execute-api.us-east-1.amazonaws.com/prod/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

Delete a task:
curl -X DELETE https://zyao7mvczc.execute-api.us-east-1.amazonaws.com/prod/todos/{id}

## Deploy It Yourself

Prerequisites:
- AWS account (free tier works)
- AWS CLI configured (aws configure)
- Python 3.x

1. Create the DynamoDB table:
aws dynamodb create-table --table-name TodoItems \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

2. Create the IAM role:
aws iam create-role --role-name todo-lambda-role \
  --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name todo-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
aws iam attach-role-policy --role-name todo-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

3. Package and deploy the Lambda:
zip lambda.zip lambda_function.py
aws lambda create-function --function-name todo-api \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/todo-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip

4. Set up API Gateway:
aws apigateway create-rest-api --name todo-api --endpoint-configuration types=REGIONAL

## Stack
Lambda · API Gateway · DynamoDB · IAM · AWS CLI · Python
