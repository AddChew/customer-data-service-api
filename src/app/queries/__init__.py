from strawberry import type, field
from src.app.database import database
from src.app.schemas.customer import Customer
from src.app.authorization import IsAuthorized


permission_classes = [IsAuthorized]


@type
class Query:

    @field(permission_classes = permission_classes) # TODO: should be getCustomer, getAccount, getAccounts, getTransactions 
    def getCustomer(cif: str) -> Customer:
        return list(filter(lambda customer: customer.cif == cif, database))