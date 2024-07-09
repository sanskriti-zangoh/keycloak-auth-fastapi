from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
import jwt

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, refresh_url: str, client_id: str, client_secret: str):
        super().__init__(app)
        self.refresh_url = refresh_url
        self.client_id = client_id
        self.client_secret = client_secret

    async def refresh_access_token(self, refresh_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.refresh_url, data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            })
            if response.status_code == 200:
                return response.json()
            return None

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        if response.status_code == 401 and request.headers.get("Authorization"):  # Unauthorized, possibly due to expired token
            try:
                refresh_token = request.cookies.get("refresh_token")
                if refresh_token:
                    new_token = await self.refresh_access_token(refresh_token)
                    if new_token:
                        # Modify the request headers with the new token
                        request.headers["Authorization"] = f"Bearer {new_token['access_token']}"
                        response = await call_next(request)
                        response.set_cookie(key="access_token", value=new_token['access_token'])
                        response.set_cookie(key="refresh_token", value=new_token['refresh_token'])
                        return response
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass
        
        return response