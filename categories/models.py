from django.db import models
from common.models import CommonModel

# Create your models here.
class Category(CommonModel):
    """Room and Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = (
            "rooms",
            "Rooms",
        )
        EXPERIENCE = (
            "experience",
            "Experience",
        )

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(max_length=20, choices=CategoryKindChoices.choices)

    def __str__(self) -> str:
        return f"{self.kind.title()}:{self.name.title()}"

    class Meta:
        verbose_name_plural = "Categories"
