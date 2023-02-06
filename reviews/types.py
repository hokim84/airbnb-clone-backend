import strawberry
from strawberry import auto
import typing
from . import models
from users.types import UserType


@strawberry.django.type(models.Review)
class ReviewType:
    payload: auto
    rating: auto
