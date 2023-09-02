from typing import List
from strawberry import type, field
from src.app.database import database
from src.app.authorization import IsAuthorized
from src.app.schemas import Customer, Account, Transaction


permission_classes = [IsAuthorized]


def check_customer_exists(cif: str):
    for customer in database["customers"]:
        if customer.cif == cif:
            return customer
    raise Exception("Customer does not exist")


def check_account_exists(accNum: str):
    for account in database["accounts"]:
        if account.accNum == accNum:
            return account
    raise Exception("Account does not exist")


@type
class Query:

    @field(permission_classes = permission_classes)
    def getCustomer(cif: str) -> Customer:
        return check_customer_exists(cif)

    @field(permission_classes = permission_classes)
    def getAccount(accNum: str) -> Account:
        return check_account_exists(accNum)
    
    @field(permission_classes = permission_classes)
    def getTransaction(transId: str) -> Transaction:
        for transaction in database["transactions"]:
            if transaction.transId == transId:
                return transaction
        raise Exception("Transaction does not exist")
    
    @field(permission_classes = permission_classes)
    def getAccounts(cif: str) -> List[Account]:
        check_customer_exists(cif)
        return list(filter(lambda account: account.cif == cif, database["accounts"]))
    
    @field(permission_classes = permission_classes)
    def getTransactionsByCif(cif: str) -> List[Transaction]:
        check_customer_exists(cif)
        return list(filter(lambda transaction: transaction.cif == cif, database["transactions"]))
    
    @field(permission_classes = permission_classes)
    def getTransactionsByAccNum(accNum: str) -> List[Transaction]:
        check_account_exists(accNum)
        return list(filter(lambda transaction: transaction.accNum == accNum, database["transactions"]))  