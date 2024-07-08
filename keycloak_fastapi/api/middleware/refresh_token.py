from fastapi import Request, Response, status
from depends.auth import keycloak_openid
from starlette.middleware.base import BaseHTTPMiddleware

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        if response.status_code == 401:  # Unauthorized, possibly due to expired token
            refresh_token = request.headers.get("X-Refresh-Token")
            if refresh_token:
                try:
                    token_response = keycloak_openid.refresh_token(refresh_token)
                    new_access_token = token_response["access_token"]
                    new_refresh_token = token_response["refresh_token"]
                    
                    # Optionally set the new tokens in the response headers or cookies
                    response.headers["X-Access-Token"] = new_access_token
                    response.headers["X-Refresh-Token"] = new_refresh_token
                    
                    # Retry the request with the new access token
                    request.headers["Authorization"] = f"Bearer {new_access_token}"
                    response = await call_next(request)
                except Exception as e:
                    response = Response(
                        content=str(e),
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )
        
        return response
