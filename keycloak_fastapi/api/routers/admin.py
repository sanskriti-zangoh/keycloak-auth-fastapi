from fastapi import APIRouter, Depends, HTTPException, status
from depends.auth import get_user_info, oauth2_scheme, has_role, get_payload
from depends.auth import check_admin_role, has_role_bool, check_role
from api.schemas import User
from typing import Optional, Tuple
import requests


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def dashboard(depended_on_role: bool = Depends(has_role("admin"))):
    return {"message": f"Hello Admin"}



# @router.get("/integrated")
# async def integrated(depended_on_role: bool = Depends(has_role("admin")), user: User = Depends(get_user_info)):
#     return {"message": f"Hello Admin {user.username}"}

# @router.get("/integrated")
# async def integrated(user: User = Depends(get_user_info)):
#     return {"message": f"Hello {user.username}"}

# @router.get("/integrated")
# async def integrated():
#     return {"message": f"Hello Guest User"}

@router.get("/integrated")
async def integrated(role: str = Depends(check_admin_role), user: User = Depends(get_user_info), payload: dict = Depends(get_payload)):
    try:
        if role:
            return {
                "message": "Hello Admin",
                "data": payload
            }
        else:
            return {
                "message": "Hello User",
                "data": user
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.get("/integrated2")
async def integrated(
    is_admin: bool = Depends(lambda : check_role("admin")),  # Corrected
    user: User = Depends(get_user_info),
    payload: dict = Depends(get_payload)
):
    if is_admin:
        return {"message": "Hello Admin", "data": payload}
    else:
        return {"message": "Hello User", "data": user}
    
@router.get("integrated/final")
async def integrated(is_admin: bool = Depends(has_role_bool("admin")), user: User = Depends(get_user_info), payload: dict = Depends(get_payload)):
    try:
        if is_admin:
            return {"message": "Hello Admin", "data": payload}
        else:
            return {"message": "Hello User", "data": user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )