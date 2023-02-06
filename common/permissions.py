from strawberry.types import Info
import typing
from strawberry.permission import BasePermission


class OnlyLoggedIn(BasePermission):
    message = "you need to be logged in this"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated
