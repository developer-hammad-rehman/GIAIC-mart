from typing import Annotated
from fastapi  import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.models.app_model import EmailMessage
from app.models.db_model import User
from ..controllers.db.index import get_session
from ..controllers.crud.user_crud import get_user_by_username , create_user
from ..controllers.pwd.pwd_context import verify_hash , create_hash
from ..controllers.jwt.token import create_access_token , create_refresh_token
from dapr.clients import DaprClient

router = APIRouter()

def get_dapr():
    with DaprClient() as dapr:
        yield dapr

DBSESSION = Annotated[Session , Depends(get_session)]
DAPRSESSION = Annotated[DaprClient , Depends(get_dapr)]

@router.post('/login')
def login_route(formdata:Annotated[OAuth2PasswordRequestForm , Depends()] , session:DBSESSION , dapr:DAPRSESSION):
    user = get_user_by_username(formdata.username , session)
    if not user:
        raise HTTPException(detail="Username is Invalid" , status_code=400)
    is_password = verify_hash(formdata.password , user.password)
    if not is_password:
        raise HTTPException(detail="Password  is Invalid" , status_code=400) 
    access_token = create_access_token({"username":user.username})
    refresh_token = create_refresh_token({"username":user.username})
    new_email_message = EmailMessage(
        to_email=user.email,
        message_type="login_message"
    )
    dapr.publish_event(pubsub_name="pubsub" , topic_name="user-topic" , data_content_type="application/json" , data=new_email_message.model_dump_json())
    return {
        "access_token":access_token,
        "refresh_token":refresh_token
    }


@router.post('/register')
def register_route(request:User , session:DBSESSION , dapr:DAPRSESSION):
    user = get_user_by_username(request.username , session)
    if not user:
        hash_password = create_hash(request.password)
        new_user = User(
            username=request.username , password=hash_password , email=request.email
        )
        create_user(new_user , session)
        new_email_message = EmailMessage(
        to_email=new_user.email,
        message_type="register_message"
    )
        dapr.publish_event(pubsub_name="pubsub" , topic_name="user-topic" , data_content_type="application/json" , data=new_email_message.model_dump_json())
        return {"message":"User Sucessfully Register"}
    else:
        raise HTTPException(detail="User Already Exist" , status_code=401) 