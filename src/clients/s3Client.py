import boto3
from botocore.exceptions import NoCredentialsError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_s3_client():
    return boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id='your_access_key',
        aws_secret_access_key='your_secret_key',
        endpoint_url='http://localstack:4566'  # LocalStack S3 endpoint
    )