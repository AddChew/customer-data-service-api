from typing import List
from fastapi import HTTPException, status

from app.schemas import Transaction
from app.database.connection import transactions_collection
from app.services.queries.accounts import retrieve_accounts
from app.services.queries.customers import retrieve_customer


async def retrieve_transactions(refId: str = None, cif: str = None, accNum: str = None, transaction_type: str = None) -> List[Transaction]:
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
        await retrieve_customer(cif)
        if isinstance(prefix, tuple):
            filters["$or"] = [{f"{p}Cif": {"$eq": cif}} for p in prefix]
        else:
            filters[f"{prefix}Cif"] = cif

    if accNum:
        await retrieve_accounts(cif, accNum)
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
        detail = "Transaction does not exist.",
    )