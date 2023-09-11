from datetime import date
from pydantic import BaseModel


class Account(BaseModel):
    """
    Account Schema.
    """
    _id: str
    accNum: str
    accHolderCif: str
    accHolderName: str
    accType: str
    currency: str
    createDate: date
    accStatus: str