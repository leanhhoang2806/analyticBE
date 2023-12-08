from dataclasses import dataclass
import logging
import jwt

# Auth0 configuration
AUTH0_DOMAIN = "dev-1wecvjynzqyw78g0.us.auth0.com"
API_IDENTIFIER = "https://dev-1wecvjynzqyw78g0.us.auth0.com/api/v2/"
ISSUER=f"https://{AUTH0_DOMAIN}/"
logging.basicConfig(level=logging.INFO)


@dataclass
class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    jwt_access_token: str
    auth0_issuer_url: str = ISSUER
    auth0_audience: str = API_IDENTIFIER
    algorithm: str = "RS256"
    jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"

    def validate(self):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.jwt_access_token
            ).key
            payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
            )
        except Exception:
            raise Exception("Invalid token")
        return payload