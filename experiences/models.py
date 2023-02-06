from django.db import models
from common.models import CommonModel

# Create your models here.
class Experience(CommonModel):

    """Experience Model definition"""

    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    name = models.CharField(max_length=250)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    description = models.CharField(
        max_length=250,
    )
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    explanation = models.TextField()

    def __str__(self) -> str:
        return self.name
