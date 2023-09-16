from strawberry import field
from app.schemas import Customer
from strawberry.types import Info

from app.commons import set_status_code
from strawberry.http.exceptions import HTTPException
from app.database.connection import customers_collection
from app.services.authorization import permission_classes


@field(permission_classes = permission_classes)
@set_status_code
async def retrieveCustomer(cif: str, info: Info) -> Customer:
    """
    Retrieve customer details if it exists in the database.

    Args:
        cif (str): Cif of customer to query from database.
        info (Info): Request and response information.

    Raises:
        HTTPException: Raised when customer does not exist.

    Returns:
        Customer: Customer object.
    """
    customer = await customers_collection.find_one({"cif": cif})
    if customer:
        return Customer(**customer)
    raise HTTPException(
        status_code = 404,
        reason = "Customer does not exist"
    )