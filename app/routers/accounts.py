from typing import List
from fastapi import APIRouter

from app.services import queries
from app.schemas import Account, Message
from fastapi import HTTPException, status


router = APIRouter(
    prefix = "/accounts",
    tags = ["Accounts"],
    responses = {401: {"model": Message}, 404: {"model": Message}},
)


@router.get(
    path = "", 
    summary = "Retrieve Account(s) Details", 
    description = "Retrieve account(s) details by cif and/or accNum."
)
async def read_accounts(cif: str = None, accNum: str = None) -> List[Account]:
    """
    Retrieve account(s) details by cif and/or accNum.

    Args:
        cif (str, optional): Cif of customer to retrieve accounts(s) for. Defaults to None.
        accNum (str, optional): Account number of account to retrieve. Defaults to None.

    Raises:
        HTTPException: Raised when both cif and accNum are missing from the query parameters.

    Returns:
        List[Account]: List of Account objects.
    """
    if cif is None and accNum is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Missing cif and/or accNum in query parameters."
        )
    return await queries.retrieve_accounts(
        cif = cif,
        accNum = accNum,
    )