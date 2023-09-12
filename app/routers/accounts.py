from typing import List
from fastapi import APIRouter
from app.services import queries
from app.schemas.account import Params
from app.schemas import Account, Message


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
async def read_accounts(params: Params) -> List[Account]:
    """
    Retrieve account(s) details by cif and/or accNum.

    Args:
        params (Params): Query params consisting of cif and/or accNum.

    Returns:
        List[Account]: List of Account objects.
    """
    return await queries.retrieve_accounts(
        cif = params.cif,
        accNum = params.accNum,
    )