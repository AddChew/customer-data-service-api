from pydantic import BaseModel


class Message(BaseModel):
    """
    Message Response Schema.
    """
    detail: str