from pyexpat import model
from unittest import mock
from django.db import models

# Create your models here.
class House(models.Model):

    """Model Definition for Housess"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField()
    description = models.TextField()
    address = models.TextField(max_length=140)
    pet_allowed = models.BooleanField(default=True, help_text="mong mong!")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name
