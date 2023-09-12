from fastapi import APIRouter
from app.services import queries
from app.schemas import Customer, Message


router = APIRouter(
    prefix = "/customers",
    tags = ["Customers"],
    responses = {401: {"model": Message}, 404: {"model": Message}},
)


@router.get(
    path = "", 
    summary = "Retrieve Customer Details", 
    description = "Retrieve customer details by cif."
)
async def read_customer(cif: str) -> Customer:
    """
    Retrieve customer details by cif.

    Args:
        cif (str): Cif of customer to retrieve details on.

    Returns:
        Customer: Customer object.
    """
    return await queries.retrieve_customer(cif)