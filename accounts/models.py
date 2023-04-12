from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    address = models.TextField(null=True)
    phone_number = models.BigIntegerField(validators=[MinValueValidator(12),
                                                      MaxValueValidator(12)],
                                          null=True,
                                          unique=True)
    birth_date = models.DateField(null=True)
    bio = models.TextField(null=True)
    credit = models.IntegerField(default=0)
    purchased_magazine = ArrayField(models.IntegerField(), null=True)
    point = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to="accounts/profile_pictures",
                                        default="accounts/profile_pictures/default_profile_pic.png")


class Transaction(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_success = models.BooleanField()
    price = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
