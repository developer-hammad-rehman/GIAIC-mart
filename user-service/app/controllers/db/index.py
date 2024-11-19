from ...settings import DATABASE_URL
from sqlmodel import create_engine , Session , SQLModel


connection_string = DATABASE_URL.replace("postgresql" , "postgresql+psycopg")

engine = create_engine(connection_string , echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(engine)