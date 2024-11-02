import json
import os

import boto3
import pytest
from dotenv import load_dotenv
from moto import mock_aws

from src.text_analysis.lambda_function import lambda_handler

load_dotenv()

dynamodb_table = os.getenv('DYNAMODB_TABLE')
s3_bucket = os.getenv('S3_BUCKET')

@pytest.fixture
def aws_resources():
    """Setup mock DynamoDB and S3 resources using moto."""
    with mock_aws():
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        dynamodb.create_table(
            TableName=os.getenv('DYNAMODB_TABLE'),
            KeySchema=[
                {'AttributeName': 'LogID', 'KeyType': 'HASH'},
                {'AttributeName': 'Timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'LogID', 'AttributeType': 'S'},
                {'AttributeName': 'Timestamp', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=os.getenv('S3_BUCKET'))

        yield dynamodb, s3

def test_lambda_handler_success(aws_resources):
    """Test successful execution of lambda_handler."""
    event = {
        'logId': 'test-log-id',
        'timestamp': '2024-11-01T12:00:00Z',
        'originalText': 'Test original text',
        'analyzedText': 'Test analyzed text',
        'sentimentScore': 0.85,
        'sentimentLabel': 'Positive'
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Procesamiento completado exitosamente'
    dynamodb = aws_resources[0]
    result = dynamodb.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={
            'LogID': {'S': 'test-log-id'},
            'Timestamp': {'S': '2024-11-01T12:00:00Z'}
        }
    )
    assert 'Item' in result
    s3 = aws_resources[1]
    s3_object = s3.get_object(
        Bucket=os.getenv('S3_BUCKET'),
        Key=f"{event['logId']}/{event['timestamp']}.json"
    )
    stored_data = json.loads(s3_object['Body'].read().decode())
    assert stored_data['originalText'] == event['originalText']
    assert stored_data['analyzedText'] == event['analyzedText']

def test_lambda_handler_error(aws_resources):
    """Test error handling in lambda_handler when event data is missing."""
    event = {}  
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert 'Error en el procesamiento' in json.loads(response['body'])