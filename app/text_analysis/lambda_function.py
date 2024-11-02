import json
import os
import boto3
import traceback
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event, context):
    dynamodb_client = boto3.client('dynamodb')
    s3_client = boto3.client('s3')
    table_name = os.getenv('DYNAMODB_TABLE')
    bucket_name = os.getenv('S3_BUCKET')

    try:
        log_entry = {
            'LogID': {'S': event.get('logId', '12345')},
            'Timestamp': {'S': event.get('timestamp', '2024-11-01T00:00:00Z')},
            'OriginalText': {'S': event.get('originalText', 'Texto de prueba')},
            'AnalyzedText': {'S': event.get('analyzedText', 'Texto analizado')},
            'SentimentScore': {'N': str(event.get('sentimentScore', '0.5'))},
            'SentimentLabel': {'S': event.get('sentimentLabel', 'Neutral')}
        }

        dynamodb_client.put_item(
            TableName=table_name,
            Item=log_entry
        )

        sample_content = 'Este es un contenido de prueba para el archivo de texto.'
        s3_client.put_object(
            Bucket=bucket_name,
            Key='sample.txt',
            Body=sample_content.encode()
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Procesamiento completado exitosamente')
        }

    except Exception as e:
        print(f"Error completo: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error en el procesamiento: {str(e)}')
        }
