from contextlib import asynccontextmanager
from database.session import init_db
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield