from datetime import date
from strawberry import type


@type
class Account:
    """
    Account GraphQL Type Schema.
    """
    _id: str
    accNum: str
    accHolderCif: str
    accHolderName: str
    accType: str
    currency: str
    createDate: date
    accStatus: str