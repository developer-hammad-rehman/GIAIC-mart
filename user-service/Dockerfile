FROM python:3.12-slim


RUN pip install poetry

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock /code/

RUN poetry config virtualenvs.create false


RUN poetry install


COPY . /code/


CMD ["poetry" , "run"  , "uvicorn" , "app.main:app" , "--reload" , "--host"  ,"0.0.0.0"]