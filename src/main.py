from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from src.clients.s3Client import S3Manager
import os
from src.dao.connectors import get_db
import logging
from src.validators.validators import validate_token
from src.models.auth0_user import PostDocumentPayload
from src.dao.s3_upload_files_manager import S3FilesManager
from src.models.database_models import S3File
import json
import uuid
from fastapi import UploadFile

logging.basicConfig(level=logging.INFO)
BUCKET_NAME = 'your-bucket-name'

app = FastAPI()

# Dependency to run Flyway migrations
def migrate_db():
    flyway_cmd = "flyway -url=jdbc:postgresql://db:5432/mydatabase -user=postgres -password=password -locations=filesystem:/app/flyway/sql -X migrate"
    os.system(flyway_cmd)

# Register the startup event using app.add_event_handler
app.add_event_handler("startup", migrate_db)


# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers,
    expose_headers=["*"]
)

logging.info("Initializing dependencies...")
db = get_db()
s3_file_manager = S3FilesManager(db)
logging.info("Sucessfully initialized db")
s3_manager = S3Manager(
    region_name='us-east-1',
    aws_access_key_id='your_access_key',
    aws_secret_access_key='your_secret_key',
    endpoint_url='http://localstack:4566'
)

s3_manager.create_bucket_if_not_exist(BUCKET_NAME)
logging.info("Sucessfully initialized S3 client")



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile, token: str = Depends(validate_token)):
    s3_path = s3_manager.upload_to_s3(file.file, BUCKET_NAME, file.filename)
    s3_file_manager.create_s3_file(S3File(id = uuid.uuid4(), file_name=file.filename, file_url=s3_path))
    return json.dumps({"s3_path": s3_path})

