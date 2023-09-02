from datetime import date
from strawberry import type


@type
class Transaction:
    refId: str
    fromCif: str
    fromAccNum: str
    toCif: str
    toAccNum: str
    amount: float
    currency: str
    transDate: date