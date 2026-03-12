import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TodoItems')

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']

    if method == 'POST' and path == '/todos':
        return create_todo(event)
    elif method == 'GET' and path == '/todos':
        return list_todos()
    elif method == 'PUT' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return update_todo(event, todo_id)
    elif method == 'DELETE' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return delete_todo(todo_id)
    else:
        return response(404, {'error': 'Not found'})

def create_todo(event):
    body = json.loads(event['body'])
    item = {
        'id': str(uuid.uuid4()),
        'task': body['task'],
        'done': False,
        'created_at': datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)
    return response(201, item)

def list_todos():
    result = table.scan()
    return response(200, result['Items'])

def update_todo(event, todo_id):
    body = json.loads(event['body'])
    table.update_item(
        Key={'id': todo_id},
        UpdateExpression='SET done = :d',
        ExpressionAttributeValues={':d': body['done']}
    )
    return response(200, {'message': 'Updated'})

def delete_todo(todo_id):
    table.delete_item(Key={'id': todo_id})
    return response(200, {'message': 'Deleted'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }