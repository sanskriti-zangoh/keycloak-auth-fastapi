from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/get_token")
async def get_user(token: str = Depends(oauth2_scheme)):
    return token

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
