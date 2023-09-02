from datetime import date
from strawberry import type


@type
class Account:
    accNum: str
    accHolderCif: str
    accHolderName: str
    accType: str
    currency: str
    createDate: date
    accStatus: str