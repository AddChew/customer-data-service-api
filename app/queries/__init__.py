from typing import List, Optional
from strawberry import type, field
from app.database import database
from app.authorization import IsAuthorized
from app.schemas import Customer, Account, Transaction


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


def check_transaction_type(transaction_type: str):
    if transaction_type in ("credit", "debit", None):
        return
    raise Exception("Invalid transaction_type. transaction_type takes on the value 'credit', 'debit' or null.")


@type
class Query:

    @field(permission_classes = permission_classes)
    def getCustomer(cif: str) -> Customer:
        return check_customer_exists(cif)

    @field(permission_classes = permission_classes)
    def getAccount(accNum: str) -> Account:
        return check_account_exists(accNum)
    
    @field(permission_classes = permission_classes)
    def getTransaction(refId: str) -> Transaction:
        for transaction in database["transactions"]:
            if transaction.refId == refId:
                return transaction
        raise Exception("Transaction does not exist")
    
    @field(permission_classes = permission_classes)
    def getAccounts(cif: str) -> List[Account]:
        check_customer_exists(cif)
        return list(filter(lambda account: account.accHolderCif == cif, database["accounts"]))
    
    @field(permission_classes = permission_classes)
    def getTransactionsByCif(cif: str, transaction_type: Optional[str] = None) -> List[Transaction]:
        check_transaction_type(transaction_type)
        check_customer_exists(cif)

        if transaction_type == "credit":
            return list(filter(lambda transaction: transaction.toCif == cif, database["transactions"]))

        if transaction_type == "debit":
            return list(filter(lambda transaction: transaction.fromCif == cif, database["transactions"]))
        
        return list(filter(lambda transaction: (transaction.fromCif == cif) or (transaction.toCif == cif), database["transactions"])) 

    @field(permission_classes = permission_classes)
    def getTransactionsByAccNum(accNum: str, transaction_type: Optional[str] = None) -> List[Transaction]:
        check_transaction_type(transaction_type)
        check_account_exists(accNum)

        if transaction_type == "credit":
            return list(filter(lambda transaction: transaction.toAccNum == accNum, database["transactions"]))

        if transaction_type == "debit":
            return list(filter(lambda transaction: transaction.fromAccNum == accNum, database["transactions"]))
        
        return list(filter(lambda transaction: (transaction.fromAccNum == accNum) or (transaction.toAccNum == accNum), database["transactions"]))