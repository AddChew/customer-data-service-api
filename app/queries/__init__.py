# from typing import List, Optional
# from strawberry import type, field

# from app.services.authorization import IsAuthorized
# from app.schemas import Customer, Account, Transaction
# from app.database.connection import customers_collection, accounts_collection, transactions_collection


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