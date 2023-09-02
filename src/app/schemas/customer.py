from datetime import date
from strawberry import type


@type
class Customer:
    cif: str
    name: str
    date_of_birth: date
    address: str
    nationality: str
    join_date: date 