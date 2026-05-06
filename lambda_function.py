import json
import boto3
import os
from datetime import datetime

# Connect to DynamoDB using the table name injected by Terraform
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # Get the HTTP method and path from the request
    method = event['httpMethod']
    path = event['path']

    # Route the request to the right function
    if method == 'GET' and path == '/items':
        return get_all_items()
    elif method == 'GET' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        return get_item(item_id)
    elif method == 'POST' and path == '/items':
        body = json.loads(event['body'])
        return create_item(body)
    elif method == 'DELETE' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        return delete_item(item_id)
    else:
        return response(404, {'message': 'Route not found'})


def get_all_items():
    # Scan the entire DynamoDB table and return all items
    result = table.scan()
    return response(200, result['Items'])


def get_item(item_id):
    # Look up a single item by its ID
    result = table.get_item(Key={'id': item_id})
    item = result.get('Item')
    if not item:
        return response(404, {'message': 'Item not found'})
    return response(200, item)


def create_item(body):
    # Create a new item with a timestamp
    item = {
        'id': body['id'],
        'name': body['name'],
        'created_at': datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)
    return response(201, {'message': 'Item created', 'item': item})


def delete_item(item_id):
    # Delete an item by its ID
    table.delete_item(Key={'id': item_id})
    return response(200, {'message': 'Item deleted'})


def response(status_code, body):
    # Standard API response format
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }