from datetime import date
from pydantic import BaseModel


class Transaction(BaseModel):
    """
    Transaction Response Schema.
    """
    _id: str
    refId: str
    fromCif: str
    fromAccNum: str
    toCif: str
    toAccNum: str
    amount: float
    currency: str
    transDate: date