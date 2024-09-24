import os
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    table_name = os.environ['DYNAMODB_TABLE']
    bucket_name = os.environ['S3_BUCKET']
    
    table = dynamodb.Table(table_name)
    response = table.scan()
    total_records = len(response['Items'])

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f'total_records_{timestamp}.txt'
    
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=str(total_records))

    return {
        'statusCode': 200,
        'body': json.dumps(f'Total records: {total_records}, saved to {file_name}')
    }
