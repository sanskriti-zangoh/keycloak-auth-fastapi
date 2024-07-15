from api.schemas import authConfiguration
import requests
from fastapi import HTTPException

from pydantic import BaseModel
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    id_token: str
    expires_in: int
    refresh_expires_in: int

class KeyCloakOIDC:
    def __init__(self, settings: authConfiguration):
        self.settings = settings

    async def get_code_url(self):
        authorization_url = self.settings.authorization_url
        params = {
            'client_id': self.settings.client_id,
            'redirect_uri': 'http://localhost:5000/test/token',  # Update the redirect URI if necessary
            'response_type': 'code',
            'scope': 'openid'
        }
        return requests.Request('GET', authorization_url, params=params).prepare().url

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> TokenResponse:
        token_url = self.settings.token_url
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.settings.client_id,
            'client_secret': self.settings.client_secret
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return TokenResponse(**token_data)
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
