from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import boto3

from botocore.exceptions import NoCredentialsError
from src.clients.s3Client import get_s3_client

from fastapi.security import OAuth2PasswordBearer

from src.dao.connectors import get_db
import logging
import jwt
import requests
from src.validators.request_validations import JsonWebToken

# Dependency Initialization
db = get_db()
logging.basicConfig(level=logging.INFO)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def validate_token(token: str = Depends(oauth2_scheme)):
    return JsonWebToken(token).validate()

app = FastAPI()

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), s3_client: boto3.client = Depends(get_s3_client), token: str = Depends(oauth2_scheme)):
    try:
        # Upload the file to S3
        s3_client.upload_fileobj(file.file, 'your-bucket-name', file.filename)
        return {"message": "File uploaded successfully"}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")

@app.get("/test")
async def private(token: str = Depends(validate_token)):
    return {"user": token}