from fastapi import FastAPI
from app.models.app_model import CloudEventModel
from .routes.user_routes import router
from .models.db_model import *
from .controllers.db.index import create_tables
from contextlib import asynccontextmanager
from dapr.ext.fastapi import DaprApp



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
dapr_app = DaprApp(app)


@app.get('/')
def read_root():
    return {"message":"User Service"}


app.include_router(router)
@dapr_app.subscribe(pubsub="pubsub" , topic="user-topic")
def event_listner(data:CloudEventModel):
    print(data)