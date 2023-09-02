from datetime import date
from strawberry import type


@type
class Customer:
    cif: str
    name: str
    dateOfBirth: date
    address: str
    nationality: str
    joinDate: date 