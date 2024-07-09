from fastapi import Request, Response
from fastapi.middleware import Middleware
from datetime import datetime, timedelta, timezone
import requests
import jwt

class TokenRefreshMiddleware:
    def __init__(self, app, refresh_url: str, client_id: str, client_secret: str):
        self.app = app
        self.refresh_url = refresh_url
        self.client_id = client_id
        self.client_secret = client_secret

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            request = Request(scope, receive)
            if "authorization" in request.headers and request.headers["authorization"].startswith("Bearer"):
                token = request.headers["authorization"].split(" ")[1]
                try:
                    refresh_token = request.cookies.get("refresh_token")
                    new_token = self.refresh_access_token(refresh_token)
                    if new_token:
                        # Modify the request headers with the new token
                        scope['headers'] = [(b'authorization', f"Bearer {new_token['access_token']}".encode())] + [
                            (key, value) for key, value in scope['headers'] if key != b'authorization'
                        ]
                        response = Response("Internal server error", status_code=500)
                        response.set_cookie(key="access_token", value=new_token['access_token'])
                        response.set_cookie(key="refresh_token", value=new_token['refresh_token'])
                        await response(scope, receive, send)
                        return
                except jwt.ExpiredSignatureError:
                    pass
                except jwt.InvalidTokenError:
                    pass
        
        await self.app(scope, receive, send)

    def refresh_access_token(self, refresh_token):
        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        token_response = requests.post(self.refresh_url, data=token_data)
        if token_response.status_code == 200:
            return token_response.json()
        return None

