from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ContactUs(models.Model):
    phone_number = models.BigIntegerField(validators=[MinValueValidator(12), MaxValueValidator(12)], null=False)
    body = models.TextField(null=False)
