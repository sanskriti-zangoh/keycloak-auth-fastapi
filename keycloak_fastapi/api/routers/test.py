from depends.oidc import KeyCloakOIDC
from api.schemas import authConfiguration

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
import requests


settings = authConfiguration(
    server_url="http://keycloak:8080",
    realm="keyauth",
    client_id="open_id_client",
    client_secret="9LfRz2LmaEK61Qj8Nzgh3dxe1jpB8LVk",
    authorization_url="http://localhost:8080/realms/keyauth/protocol/openid-connect/auth",
    token_url="http://localhost:8080/realms/keyauth/protocol/openid-connect/token",
    refresh_url="http://localhost:8080/realms/keyauth/protocol/openid-connect/token"
)

open_id = KeyCloakOIDC(settings)

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/code")
async def get_code():
    code_url = await open_id.get_code_url()
    return RedirectResponse(code_url)

from pydantic import BaseModel
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    id_token: str
    expires_in: int
    refresh_expires_in: int

@router.get("/token")
async def get_token(request: Request):
    query_params = request.query_params
    code = query_params['code']
    print(f"Authorization code: {code}") 
    client_id = settings.client_id
    client_secret = settings.client_secret
    redirect_uri = "http://localhost:5000/test/token"
    
    token_url = "http://keycloak:8080/realms/keyauth/protocol/openid-connect/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return TokenResponse(**token_data)
        else:
            return {"error": "Failed to retrieve token",
                    "details": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

