
from fastapi import Depends
from src.validators.request_validations import JsonWebToken

import logging

logging.basicConfig(level=logging.INFO)



def get_bearer_token(request) -> str:
    logging.error(f"Request headers: {request.headers}")
    authorization_header = request.headers.get("Authorization")
    token = authorization_header.split()[1]
    if authorization_header:
        return token
    else:
        raise Exception("Authorization header not found")


def validate_token(token: str = Depends(get_bearer_token)):
    logging.error(f"Validating token: {token}")
    return JsonWebToken(token).validate()