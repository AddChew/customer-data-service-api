from typing import Callable
from functools import wraps
from strawberry.http.exceptions import HTTPException


def set_status_code(method: Callable) -> Callable:
    """
    Decorator to overwrite response status code with the specified
    status code in HTTPException if HTTPException is raised.

    Args:
        method (Callable): Method to decorate.

    Raises:
        Exception: Raised when HTTPException is raised in method.

    Returns:
        Callable: Modified method.
    """
    @wraps(method)
    async def wrapper(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except HTTPException as error:
            info = kwargs.get('info')
            info.context['response'].status_code = error.status_code
            raise Exception(error.reason)
    return wrapper