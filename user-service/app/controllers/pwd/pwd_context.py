from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def create_hash(plain_password:str) -> str:
    return pwd_context.hash(plain_password)


def verify_hash(plain_password:str , hash_password:str) -> bool:
    return pwd_context.verify(plain_password , hash_password)