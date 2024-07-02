from fastapi import APIRouter, Depends
from depends import valid_access_token

router = APIRouter(prefix="/auth", tags=["auth"])



@router.get("/secure-endpoint")
async def secure_endpoint(current_user: dict = Depends(valid_access_token)):
    return {"message": "Secure content", "user": current_user}

@router.post("/signup/password")
async def signup_password():
    return {"message": "Signup with password"}

@router.post("/login/password")
async def login_password():
    return {"message": "Login with password"}

@router.post("/login/google")
async def login_google():
    return {"message": "Login with google"}

@router.post("/login/github")
async def login_github():
    return {"message": "Login with github"}