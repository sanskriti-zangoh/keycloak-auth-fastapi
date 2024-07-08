from fastapi import APIRouter, Depends
from api.schemas import User
from depends.auth import get_user_info

router = APIRouter(prefix="/stackauth", tags=["stackauth"])

@router.get("/secure")
async def root(user: User = Depends(get_user_info)):
    return {"message": f"Hello {user.username} you have the following service: {user.realm_roles}"}
