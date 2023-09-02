import os

from typing import Any, Awaitable
from strawberry.types.info import Info
from strawberry.permission import BasePermission


access_key = os.getenv('ACCESS_KEY')


class IsAuthorized(BasePermission):
    message = "Missing or invalid access key in request headers"

    async def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool | Awaitable[bool]:
        request = info.context['request']
        return request.headers.get('access_key') == access_key