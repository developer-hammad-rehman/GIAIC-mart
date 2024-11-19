from sqlmodel import Session , select
from ...models.db_model import User


def get_user_by_username(username:str , session:Session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        return None
    return user
 



def create_user(user:User , session:Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return "User Added"