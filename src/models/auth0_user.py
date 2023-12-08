from pydantic import BaseModel, EmailStr
from fastapi import UploadFile

class Auth0User(BaseModel):
    email: EmailStr
    email_verified: bool
    family_name: str
    given_name: str
    locale: str
    name: str
    nickname: str
    picture: str
    sub: str
    updated_at: str

class PostDocumentPayload(BaseModel):
    file: UploadFile