from app.services.queries.accounts import retrieveAccounts
from app.services.queries.customers import retrieveCustomer


queries = [
    retrieveCustomer,
    retrieveAccounts,
]