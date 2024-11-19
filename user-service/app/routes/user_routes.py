from typing import Annotated
from fastapi  import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.models.db_model import User
from ..controllers.db.index import get_session
from ..controllers.crud.user_crud import get_user_by_username , create_user
from ..controllers.pwd.pwd_context import verify_hash , create_hash
from ..controllers.jwt.token import create_access_token , create_refresh_token

router = APIRouter()

DBSESSION = Annotated[Session , Depends(get_session)]


@router.post('/login')
def login_route(formdata:Annotated[OAuth2PasswordRequestForm , Depends()] , session:DBSESSION):
    user = get_user_by_username(formdata.username , session)
    if not user:
        raise HTTPException(detail="Username is Invalid" , status_code=401)
    is_password = verify_hash(formdata.password , user.password)
    if not is_password:
        raise HTTPException(detail="Password  is Invalid" , status_code=401) 
    access_token = create_access_token({"username":user.username})
    refresh_token = create_refresh_token({"username":user.username})
    return {
        "access_token":access_token,
        "refresh_token":refresh_token
    }


@router.post('/register')
def register_route(formdata:Annotated[OAuth2PasswordRequestForm , Depends()] , session:DBSESSION):
    user = get_user_by_username(formdata.username , session)
    if not user:
        hash_password = create_hash(formdata.password)
        new_user = User(
            username=formdata.username , password=hash_password
        )
        create_user(new_user , session)
        return {"message":"User Sucessfully Register"}
    else:
        raise HTTPException(detail="User Already Exist" , status_code=401) 