
from api.schemas import authConfiguration, User
from uuid import UUID
import requests


settings = authConfiguration(
    server_url="http://keycloak:8080/",
    realm="keyauth",
    client_id="open_id_client",
    client_secret="iXEtOaTA7E6Zx58SXqvr1jYP30unYCQm",
    authorization_url="http://localhost:8080/realms/keyauth/protocol/openid-connect/auth",
    token_url="http://localhost:8080/realms/keyauth/protocol/openid-connect/token",
)
#/auth.py
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID # pip require python-keycloak
from fastapi import Security, HTTPException, status, Depends
import jwt

# This is used for fastapi docs authentification
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.authorization_url,
    tokenUrl=settings.token_url,
    scopes={"offline_access": "Access refresh token"},
    refreshUrl=settings.token_url
)

# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,  # https://sso.example.com/auth/
    client_id=settings.client_id,  # backend-client-id
    realm_name=settings.realm,  # example-realm
    client_secret_key=settings.client_secret,  # your backend client secret
    verify=True
)

async def get_idp_public_key():
    public_key = keycloak_openid.public_key()
    if not public_key.startswith("-----BEGIN PUBLIC KEY-----"):
        public_key = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"
    return public_key

# Get the payload/token from keycloak
async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        public_key = await get_idp_public_key()
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.client_id,
            options={"verify_aud": False}  # This should work now
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

# Get user infos from the payload
async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            email_verified=payload.get("email_verified"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("resource_access", {}).get(settings.client_id, {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_user_id(payload: dict = Depends(get_payload)) -> UUID:
    try:
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_realm_management_access_token() -> str:
    try: 
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin"
        token_url = f"{settings.server_url}/realms/{settings.realm}/protocol/openid-connect/token"
        token_data = {
            'username': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD,
            'grant_type': 'client_credentials',
            'client_id': settings.client_id,
            'client_secret': settings.client_secret
        }
        
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code != 200:
            raise HTTPException(status_code=token_response.status_code, detail="Failed to obtain access token")

        access_token = token_response.json().get('access_token')

        return access_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
