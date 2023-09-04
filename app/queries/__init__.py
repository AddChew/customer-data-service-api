from typing import List, Optional
from strawberry import type, field

from app.authorization import IsAuthorized
from app.schemas import Customer, Account, Transaction
from app.database.connection import customers_collection, accounts_collection, transactions_collection


permission_classes = [IsAuthorized]


async def check_customer_exists(cif: str):
    customer = await customers_collection.find_one({"cif": cif})
    if customer:
        return Customer(**customer)
    raise Exception("Customer does not exist")


async def check_account_exists(accNum: str):
    account = await accounts_collection.find_one({"accNum": accNum})
    if account:
        return Account(**account)
    raise Exception("Account does not exist")


def check_transaction_type(transaction_type: str):
    if transaction_type in ("credit", "debit", None):
        return
    raise Exception("Invalid transaction_type. transaction_type takes on the value 'credit', 'debit' or null.")


@type
class Query:

    @field(permission_classes = permission_classes)
    async def getCustomer(cif: str) -> Customer:
        return await check_customer_exists(cif)

    @field(permission_classes = permission_classes)
    async def getAccount(accNum: str) -> Account:
        return await check_account_exists(accNum)
    
    @field(permission_classes = permission_classes)
    async def getTransaction(refId: str) -> Transaction:
        transaction = await transactions_collection.find_one({"refId": refId})
        if transaction:
            return Transaction(**transaction)
        raise Exception("Transaction does not exist")
    
    @field(permission_classes = permission_classes)
    async def getAccounts(cif: str) -> List[Account]:
        await check_customer_exists(cif)
        accounts = accounts_collection.find({"accHolderCif": cif})
        return [Account(**account) async for account in accounts]    
    
    @field(permission_classes = permission_classes)
    async def getTransactionsByCif(cif: str, transaction_type: Optional[str] = None) -> List[Transaction]:
        await check_transaction_type(transaction_type)
        await check_customer_exists(cif)

        if transaction_type == "credit":
            filters = {"toCif": cif}
            
        elif transaction_type == "debit":
            filters = {"fromCif": cif}

        else:
            filters = {
                { 
                    "$or": [
                        {"fromCif": { "$eq": cif }}, 
                        {"toCif": { "$eq": cif }},
                    ]
                }
            }
        return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]

    @field(permission_classes = permission_classes)
    async def getTransactionsByAccNum(accNum: str, transaction_type: Optional[str] = None) -> List[Transaction]:
        await check_transaction_type(transaction_type)
        await check_account_exists(accNum)

        if transaction_type == "credit":
            filters = {"toAccNum": accNum}
            
        elif transaction_type == "debit":
            filters = {"fromAccNum": accNum}

        else:
            filters = {
                { 
                    "$or": [
                        {"fromAccNum": { "$eq": accNum }}, 
                        {"toAccNum": { "$eq": accNum }},
                    ]
                }
            }
        return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]