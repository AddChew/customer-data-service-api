import os

from typing import Any, Awaitable
from strawberry.types.info import Info
from strawberry.permission import BasePermission


accessKey = os.getenv('ACCESS_KEY', 'test')


class IsAuthorized(BasePermission):
    """
    Permission class to check if a user is permitted to access the resource.
    """
    message = "Missing or invalid access key in request headers"

    async def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool | Awaitable[bool]:
        """
        Method to check if a user is permitted to access the resource. If a user is permitted, the
        accessKey in his request headers should be valid.

        Returns:
            bool | Awaitable[bool]: True if the accessKey in the request headers is valid, otherwise False.
        """
        request = info.context['request']
        return request.headers.get('accessKey') == accessKey