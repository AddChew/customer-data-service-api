from datetime import date
from pydantic import BaseModel


class Customer(BaseModel):
    """
    Customer Response Schema.
    """
    _id: str
    cif: str
    name: str
    dateOfBirth: date
    address: str
    nationality: str
    joinDate: date 