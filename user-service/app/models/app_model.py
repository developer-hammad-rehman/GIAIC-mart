from typing import Literal
from pydantic import BaseModel


class EmailMessage(BaseModel):
    to_email : str
    message_type : Literal["login_message" , "register_message"]


class CloudEventModel(BaseModel):
    data: EmailMessage
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str