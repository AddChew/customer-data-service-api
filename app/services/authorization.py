import os

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, status


access_key = os.getenv('ACCESS_KEY', 'test')
access_key_header = APIKeyHeader(name = "accessKey", auto_error = False)


async def verify_access_key(access_key_header: str = Security(access_key_header)):
    """
    Verify the validity of the accessKey provided in the request headers. 
    
    Used to check if a user is permitted to access the resource. If a user is permitted, the 
    accessKey in his request headers should be valid.

    Args:
        access_key_header (str, optional): _description_. Defaults to Security(access_key_header).

    Raises:
        HTTPException: Raised when the accessKey in the request headers is invalid.
    """
    if access_key_header != access_key:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Missing or invalid access key in request headers",
        )