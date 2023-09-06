from datetime import date
from strawberry import type


@type
class Transaction:
    """
    Transaction GraphQL Type Schema.
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