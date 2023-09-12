from datetime import date
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, root_validator


class Account(BaseModel):
    """
    Account Response Schema.
    """
    _id: str
    accNum: str
    accHolderCif: str
    accHolderName: str
    accType: str
    currency: str
    createDate: date
    accStatus: str


@dataclass
class Params:
    cif: Optional[str] = None
    accNum: Optional[str] = None

    @root_validator
    def check_cif_or_accNum(cls, v):
        if not any(v.values()):
            raise ValueError("Missing cif and/or accNum in query params")
        return v