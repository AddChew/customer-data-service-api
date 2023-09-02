from datetime import date
from src.app.schemas import Customer, Account, Transaction


customers = [
    Customer(
        cif = "00000001", name = "Bobby Tan", dateOfBirth = date(1995, 10, 2), address = 'address 1', nationality = 'SG', joinDate = date(2000, 1, 1)
    ),
    Customer(
        cif = "00000002", name = "Sally Chan", dateOfBirth = date(1959, 11, 4), address = 'address 2', nationality = 'MY', joinDate = date(2003, 2, 13)
    ),    
]

accounts = [
    Account(
        accNum = "10000001", accHolderCif = "00000001", accHolderName = "Bobby", accType = "SAVINGS", currency = "SGD", createDate = date(2000, 1, 1), accStatus = "ACTIVE"
    ),
    Account(
        accNum = "10000002", accHolderCif = "00000002", accHolderName = "Sally", accType = "CURRENT", currency = "SGD", createDate = date(2003, 2, 14), accStatus = "ACTIVE"
    ),
]

transactions = [
    Transaction(
        refId = "1001001", fromCif = "00000001", fromAccNum = "10000001", toCif = "00000002", toAccNum = "10000002", amount = 1000, currency = "SGD", transDate = date(2023, 9, 2)
    )
]

database = {
    "customers": customers,
    "accounts": accounts,
    "transactions": transactions,
}

# TODO: create dummy data
# TODO: setup mongodb container
# TODO: initial data load into mongodb
# TODO: integrate graphql with mongodb
# TODO: move fastapi into docker