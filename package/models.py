from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(null=True, upload_to="package/package_images")
