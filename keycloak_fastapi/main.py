# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.myauth import router as myauth_router


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

app.include_router(myauth_router)