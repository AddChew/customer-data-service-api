from fastapi import status
from strawberry import field
from app.schemas import Account

from strawberry.types import Info
from typing import List, Optional
from app.commons import set_status_code

from strawberry.http.exceptions import HTTPException
from app.database.connection import accounts_collection
from app.services.authorization import permission_classes
from app.services.queries.customers import _retrieveCustomer


async def _retrieveAccounts(cif: Optional[str] = None, accNum: Optional[str] = None) -> List[Account]:
    """
    Retrieve list of accounts by cif and/or accNum.

    Args:
        cif (Optional[str], optional): Cif of customer to retrieve accounts(s) for. Defaults to None.
        accNum (Optional[str], optional): Account number of account to query from database. Defaults to None.

    Raises:
        HTTPException: Raised when account does not exist.

    Returns:
        List[Account]: List of Account objects.
    """
    filters = {}
    if cif:
        await _retrieveCustomer(cif = cif)
        filters["accHolderCif"] = cif

    if accNum:
        filters["accNum"] = accNum

    accounts = [Account(**account) async for account in accounts_collection.find(filters)]
    if accounts:
        return accounts
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        reason = "Account does not exist."
    )


@field(permission_classes = permission_classes)
@set_status_code
async def retrieveAccounts(cif: Optional[str] = None, accNum: Optional[str] = None, info: Info = None) -> List[Account]:
    """
    Retrieve accounts(s) details by cif and/or accNum.

    Args:
        cif (Optional[str], optional): Cif of customer to retrieve accounts(s) for. Defaults to None.
        accNum (Optional[str], optional): Account number of account to retrieve. Defaults to None.
        info (Info, optional): Request and response information. Defaults to None.

    Raises:
        HTTPException: Raised when both cif and accNum are missing from query parameters.

    Returns:
        List[Account]: List of Account objects.
    """
    if not any((cif, accNum)):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            reason = "Missing cif and/or accNum in query parameters."
        )
    return await _retrieveAccounts(cif = cif, accNum = accNum)