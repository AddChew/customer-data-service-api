from fastapi import status
from strawberry import field
from strawberry.types import Info

from typing import List, Optional
from app.schemas import Transaction
from app.commons import set_status_code

from strawberry.http.exceptions import HTTPException
from app.services.authorization import permission_classes
from app.database.connection import transactions_collection

from app.services.queries.accounts import _retrieveAccounts
from app.services.queries.customers import _retrieveCustomer


async def _retrieveTransactions(refId: str = None, cif: str = None, accNum: str = None, transaction_type: str = None) -> List[Transaction]:
    """
    Retrieve list of transactions by refId, cif, accNum and transaction_type.

    Args:
        refId (str, optional): Transaction reference id of transaction to retrieve. Defaults to None.
        cif (str, optional): Cif of customer to retrieve transactions for. Defaults to None.
        accNum (str, optional): Account number of customer to retrieve transactions for. Defaults to None.
        transaction_type (str, optional): Transaction type. Takes on the values "credit", "debit" or None. Defaults to None.

    Raises:
        HTTPException: Raised when transaction does not exist.

    Returns:
        List[Transaction]: List of Transaction objects.
    """
    prefix_map = {
        "credit": "to",
        "debit": "from",
        None: ("to", "from"), 
    }
    prefix = prefix_map[transaction_type]

    filters = {}
    if cif:
        await _retrieveCustomer(cif)
        if isinstance(prefix, tuple):
            filters["$or"] = [{f"{p}Cif": {"$eq": cif}} for p in prefix]
        else:
            filters[f"{prefix}Cif"] = cif

    if accNum:
        await _retrieveAccounts(cif, accNum)
        if isinstance(prefix, tuple):
            filters["$or"] = [{f"{p}AccNum": {"$eq": accNum}} for p in prefix]
        else:
            filters[f"{prefix}AccNum"] = accNum

    if refId:
        filters["refId"] = refId

    transactions = [Transaction(**transaction) async for transaction in transactions_collection.find(filters)]
    if transactions:
        return transactions
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        reason = "Transaction does not exist.",
    )


@field(permission_classes = permission_classes)
@set_status_code
async def retrieveTransactions(
    refId: Optional[str] = None, cif: Optional[str] = None, accNum: Optional[str] = None, 
    transaction_type: Optional[str] = None, info: Info = None) -> List[Transaction]:
    """
    Retrieve transaction(s) details by refId, cif, accNum and transction type.

    Args:
        refId (str, optional): Reference id of the transaction to retrieve. Defaults to None.
        cif (str, optional): Cif of the transaction to retrieve. Defaults to None.
        accNum (str, optional): Account number of the transaction to retrieve. Defaults to None.
        transaction_type (str, optional): Transaction type to retrieve. Takes on the values "credit", "debit" or None. 
            If None, will retrieve both credit and debit transactions. Defaults to None.
        info (Info, optional): Request and response information. Defaults to None.

    Raises:
        HTTPException: Raised when refId, cif and accNum are all missing from the query parameters.
        HTTPException: Raised when transaction_type is not one of "credit", "debit" or None.

    Returns:
        List[Account]: List of Transaction objects.
    """
    if not any((refId, cif, accNum)):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            reason = "Missing refId, cif and/or accNum in query parameters.",
        )

    if transaction_type not in ("credit", "debit", None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            reason = "Invalid transaction_type in query params. transaction_type takes on the value 'credit', 'debit' or null.",
        )
    
    return await _retrieveTransactions(
        refId = refId,
        cif = cif,
        accNum = accNum,
        transaction_type = transaction_type,
    )