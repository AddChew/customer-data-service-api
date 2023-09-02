from typing import List, Optional
from strawberry import type, field

from src.app.database import database
from src.app.schemas.customer import Customer
from src.app.authorization import IsAuthorized


@type
class Query:

    @field(permission_classes = [IsAuthorized])
    def customers(self, cif: Optional[str] = None) -> List[Customer]:
        if cif:
            return list(filter(lambda customer: customer.cif == cif, database))
        return database