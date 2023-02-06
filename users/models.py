from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("KR", "Korea")
        EN = ("EN", "English")

    class CurrencyChoice(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("USD", "Dollar")

    real_name = models.CharField(max_length=40, default="홍길동")
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    avatar = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, null=True, choices=GenderChoices.choices)
    language = models.CharField(
        max_length=20, null=True, choices=LanguageChoices.choices
    )
    currency = models.CharField(
        max_length=10, null=True, choices=CurrencyChoice.choices
    )
