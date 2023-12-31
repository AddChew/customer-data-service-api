from datetime import date
from strawberry import type


@type
class Customer:
    """
    Customer GraphQL Type Schema.
    """
    _id: str
    cif: str
    name: str
    dateOfBirth: date
    address: str
    nationality: str
    joinDate: date 