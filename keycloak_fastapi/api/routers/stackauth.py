from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from api.schemas import User
from depends.auth import get_user_info, get_payload, oauth2_scheme, get_realm_management_access_token, settings
import requests

router = APIRouter(prefix="/stackauth", tags=["stackauth"])

@router.get("/secure")
async def root(user: User = Depends(get_user_info)):
    return {"message": f"Hello {user.username} you have the following service: {user.realm_roles}"}

@router.get("/get_payload")
async def get_token_payload(token_payload: dict = Depends(get_payload)):
    return token_payload

@router.post("/token")
async def get_token(request: Request, token: str = Depends(oauth2_scheme)):
    # Extract tokens from the request
    token_data = await request.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    # Store tokens in cookies or a secure storage
    response = JSONResponse(content={"message": "Token received"})
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)
    
    return response

@router.get("/users")
async def get_users(access_token: str = Depends(get_realm_management_access_token)):

    users_url = f"{settings.server_url}/admin/realms/{settings.realm}/users"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    users_response = requests.get(users_url, headers=headers)
    if users_response.status_code != 200:
        raise HTTPException(status_code=users_response.status_code, detail="Failed to fetch users")

    return users_response.json()
