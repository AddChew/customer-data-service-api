from pydantic import BaseModel


class Message(BaseModel):
    """
    Message Schema.
    """
    detail: str