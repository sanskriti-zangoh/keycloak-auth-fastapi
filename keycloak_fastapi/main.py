# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.stackauth import router as stackauth_router
from api.routers.user import router as user_router
from api.middleware.refresh_token import TokenRefreshMiddleware


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# app.add_middleware(TokenRefreshMiddleware)
app.include_router(stackauth_router)
app.include_router(user_router)