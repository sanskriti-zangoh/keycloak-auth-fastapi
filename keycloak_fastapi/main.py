# main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

app = FastAPI()

# Read environment variables
keycloak_server_url = os.getenv('KEYCLOAK_SERVER_URL', 'http://localhost:8080/auth/')
client_id = os.getenv('KEYCLOAK_CLIENT_ID', 'your_client_id')
realm_name = os.getenv('KEYCLOAK_REALM_NAME', 'your_realm_name')
client_secret = os.getenv('KEYCLOAK_CLIENT_SECRET', 'your_client_secret')

# Configure Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=client_id,
    realm_name=realm_name,
    client_secret_key=client_secret
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{keycloak_server_url}realms/{realm_name}/protocol/openid-connect/auth",
    tokenUrl=f"{keycloak_server_url}realms/{realm_name}/protocol/openid-connect/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secure-endpoint")
async def secure_endpoint(current_user: dict = Depends(get_current_user)):
    return {"message": "Secure content", "user": current_user}
