from app.schemas import Customer
from fastapi import HTTPException, status
from app.database.connection import customers_collection


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