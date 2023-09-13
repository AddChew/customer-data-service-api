from typing import List
from fastapi import HTTPException, status

from app.schemas import Account
from app.database.connection import accounts_collection
from app.services.queries.customers import retrieve_customer


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