import os
import boto3

dynamodb_client = boto3.resource('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.resource(
        'dynamodb', endpoint_url='http://localhost:8000'
    )

APP_TABLE = os.environ['APP_TABLE']


class Repository:

    def __init__(self):
        self.table = dynamodb_client.Table(APP_TABLE)    
