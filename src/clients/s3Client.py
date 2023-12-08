import boto3
from botocore.exceptions import ClientError
import os
import uuid
import shutil
from tempfile import NamedTemporaryFile
import logging
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)

class S3Manager:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, endpoint_url):
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url
        )

    def create_bucket_if_not_exist(self, bucket_name):
        try:
            # Check if the bucket exists
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            # If the bucket does not exist, create it
            self.s3_client.create_bucket(Bucket=bucket_name)

    def upload_to_s3(self, file, bucket_name, file_name):
        try:
            with NamedTemporaryFile(delete=False) as temp_file:
                shutil.copyfileobj(file, temp_file)

            # Upload the temporary file to S3
            key = file_name + str(uuid.uuid4())
            self.s3_client.upload_file(temp_file.name, bucket_name, key)

            # Remove the temporary file after uploading
            os.unlink(temp_file.name)
            s3_path = f"s3://{bucket_name}/{key}"

            return s3_path
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS credentials not available")