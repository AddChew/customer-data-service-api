from app.services.queries.accounts import retrieveAccounts
from app.services.queries.customers import retrieveCustomer
from app.services.queries.transactions import retrieveTransactions


queries = [
    retrieveCustomer,
    retrieveAccounts,
    retrieveTransactions,
]