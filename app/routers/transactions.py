from typing import List
from fastapi import APIRouter

from fastapi import HTTPException, status
from app.schemas import Transaction, Message
from app.services.queries.transactions import retrieve_transactions


router = APIRouter(
    prefix = "/transactions",
    tags = ["Transactions"],
    responses = {401: {"model": Message}, 404: {"model": Message}},
)


@router.get(
    path = "", 
    summary = "Retrieve Transaction(s) Details", 
    description = "Retrieve transaction(s) details by refId, cif, accNum and transaction type."
)
async def read_transactions(refId: str = None, cif: str = None, accNum: str = None, transaction_type: str = None) -> List[Transaction]:
    """
    Retrieve transaction(s) details by refId, cif, accNum and transction type.

    Args:
        refId (str, optional): Reference id of the transaction to retrieve. Defaults to None.
        cif (str, optional): Cif of the transaction to retrieve. Defaults to None.
        accNum (str, optional): Account number of the transaction to retrieve. Defaults to None.
        transaction_type (str, optional): Transaction type to retrieve. Takes on the values "credit", "debit" or None. 
            If None, will retrieve both credit and debit transactions. Defaults to None.

    Raises:
        HTTPException: Raised when refId, cif and accNum are all missing from the query parameters.
        HTTPException: Raised when transaction_type is not one of "credit", "debit" or None.

    Returns:
        List[Transaction]: List of Transaction objects.
    """
    if not any((refId, cif, accNum)):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Missing refId, cif and/or accNum in query parameters.",
        )

    if transaction_type not in ("credit", "debit", None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid transaction_type in query params. transaction_type takes on the value 'credit', 'debit' or null.",
        )
    
    return await retrieve_transactions(
        refId = refId,
        cif = cif,
        accNum = accNum,
        transaction_type = transaction_type,
    )