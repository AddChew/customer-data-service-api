from typing import List, Optional
from fastapi import HTTPException, status

from app.schemas import Customer, Account, Transaction
from app.database.connection import customers_collection, accounts_collection, transactions_collection


async def retrieve_customer(cif: str) -> Customer:
    """
    Retrieve customer details if it exists in the database.

    Args:
        cif (str): Cif of customer to query from database.

    Raises:
        HTTPException: Raised when customer does not exist.

    Returns:
        Customer: Customer object.
    """
    customer = await customers_collection.find_one({"cif": cif})
    if customer:
        return Customer(**customer)
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Customer does not exist."
    )


async def retrieve_accounts(cif: str = None, accNum: str = None) -> List[Account]:
    """
    Retrieve list of accounts by cif and/or accNum.

    Args:
        cif (str, optional): Cif of customer to retrieve accounts(s) for. Defaults to None.
        accNum (str, optional): Account number of account to query from database. Defaults to None.

    Raises:
        HTTPException: Raised when account does not exist.

    Returns:
        List[Account]: List of Account objects.
    """
    filters = {}
    if cif:
        await retrieve_customer(cif)
        filters["accHolderCif"] = cif

    if accNum:
        filters["accNum"] = accNum

    accounts = [Account(**account) async for account in accounts_collection.find(filters)]
    if accounts:
        return accounts
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Account does not exist."
    )

# def check_transaction_type(transaction_type: str | None):
#     """
#     heck if transaction type is one of "credit", "debit" or None.

#     Args:
#         transaction_type (str | None): Transaction type to check.

#     Raises:
#         Exception: Raised when transaction type is not one of "credit", "debit" or None.
#     """
#     if transaction_type in ("credit", "debit", None):
#         return
#     raise Exception("Invalid transaction_type. transaction_type takes on the value 'credit', 'debit' or null.")


# @type
# class Query:
    
#     @field(permission_classes = permission_classes)
#     async def getTransaction(refId: str) -> Transaction:
#         """
#         Retrieve transaction details based on reference id.

#         Args:
#             refId (str): Transaction reference id to retrieve information on.

#         Raises:
#             Exception: Raised when transaction does not exist.

#         Returns:
#             Transaction: Transaction object.
#         """
#         transaction = await transactions_collection.find_one({"refId": refId})
#         if transaction:
#             return Transaction(**transaction)
#         raise Exception("Transaction does not exist")
    
#     @field(permission_classes = permission_classes)
#     async def getTransactionsByCif(cif: str, transaction_type: Optional[str] = None) -> List[Transaction]:
#         """
#         Retrieve transactions by customer cif.

#         Args:
#             cif (str): Cif of customer to retrieve transactions for.
#             transaction_type (Optional[str], optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

#         Returns:
#             List[Transaction]: List of Transaction objects.
#         """
#         check_transaction_type(transaction_type)
#         await check_customer_exists(cif)

#         if transaction_type == "credit":
#             filters = {"toCif": cif}
            
#         elif transaction_type == "debit":
#             filters = {"fromCif": cif}

#         else:
#             filters = {
#                 "$or": [
#                     {"fromCif": { "$eq": cif }}, 
#                     {"toCif": { "$eq": cif }},
#                 ]
#             }
#         return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]

#     @field(permission_classes = permission_classes)
#     async def getTransactionsByAccNum(accNum: str, transaction_type: Optional[str] = None) -> List[Transaction]:
#         """
#         Retrieve transactions by account number.

#         Args:
#             accNum (str): Account number to retrieve transactions on.
#             transaction_type (Optional[str], optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

#         Returns:
#             List[Transaction]: List of Transaction objects.
#         """
#         check_transaction_type(transaction_type)
#         await check_account_exists(accNum)

#         if transaction_type == "credit":
#             filters = {"toAccNum": accNum}
            
#         elif transaction_type == "debit":
#             filters = {"fromAccNum": accNum}

#         else:
#             filters = { 
#                 "$or": [
#                     {"fromAccNum": { "$eq": accNum }}, 
#                     {"toAccNum": { "$eq": accNum }},
#                 ]
#             }
#         return [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]