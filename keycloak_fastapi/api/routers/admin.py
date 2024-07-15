from fastapi import APIRouter, Depends, HTTPException
from depends.auth import get_user_info, oauth2_scheme, has_role
from api.schemas import User
import requests


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def dashboard(depended_on_role: bool = Depends(has_role("admin"))):
    return {"message": f"Hello Admin"}