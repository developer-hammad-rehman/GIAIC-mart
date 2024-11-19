from fastapi import FastAPI
from .routes.user_routes import router
from .models.db_model import *
from .controllers.db.index import create_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def read_root():
    return {"message":"User Service"}


app.include_router(router)