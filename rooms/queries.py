from . import models
from strawberry.types import Info


def get_all_rooms(info: Info):
    return models.Room.objects.all()


def get_room(pk: int):
    return models.Room.objects.get(pk=pk)
