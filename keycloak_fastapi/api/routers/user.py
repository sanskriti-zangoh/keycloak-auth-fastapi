from depends.auth import get_user_id
from fastapi import APIRouter, Depends, HTTPException
from depends.auth import oauth2_scheme, get_realm_management_access_token, settings, get_user_info
from uuid import UUID
import requests

router = APIRouter(prefix="/user", tags=["user"])

from pydantic import BaseModel
class UpdateUser(BaseModel):
    username: str



@router.get("/get_user_id")
async def get_user_id(user_id: UUID = Depends(get_user_id)):
    return user_id

@router.get("/{user_id}")
async def get_user(user_id: UUID = Depends(get_user_id), access_token: str = Depends(get_realm_management_access_token)):

    users_url = f"{settings.server_url}/admin/realms/{settings.realm}/users/{user_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    users_response = requests.get(users_url, headers=headers)
    if users_response.status_code != 200:
        raise HTTPException(status_code=users_response.status_code, detail="Failed to fetch users")

    return users_response.json()

@router.put("/{user_id}")
async def update_user(user_id: UUID = Depends(get_user_id), access_token: str = Depends(get_realm_management_access_token), payload: dict = Depends(get_user_info)):

    users_url = f"{settings.server_url}/admin/realms/{settings.realm}/users/{user_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    users_response = requests.put(users_url, headers=headers)
    if users_response.status_code != 200:
        raise HTTPException(status_code=users_response.status_code, detail="Failed to update users")

    return users_response.json()


