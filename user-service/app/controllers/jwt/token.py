from jose import jwt
from datetime import datetime , timedelta , timezone
from ...settings import SECRET_KEY , ALGORITHM



def create_access_token(sub : dict):
    to_encode = sub.copy()
    exp_in  = datetime.now(timezone.utc) + timedelta(days=3)
    to_encode.update({"exp":exp_in})
    return jwt.encode(to_encode , key=SECRET_KEY , algorithm=ALGORITHM)


def create_refresh_token(sub : dict):
    to_encode = sub.copy()
    exp_in  = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp":exp_in})
    return jwt.encode(to_encode , key=SECRET_KEY , algorithm=ALGORITHM)
