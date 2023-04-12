from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Magazine(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    publish_date = models.DateField(auto_now_add=True)
    price = models.IntegerField()
    magazine_pdf_file = models.FileField(upload_to="magazine/magazine_pdf_files")
    cover_image = models.ImageField(upload_to="magazine/magazine_images")


class Page(models.Model):
    page_number = models.IntegerField(null=False)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    publish_date = models.DateField()
    image = models.ImageField(upload_to="magazine/page_images")
    magazine = models.ForeignKey(to=Magazine, on_delete=models.CASCADE, related_name="pages")


class Comment(models.Model):
    username = models.CharField(max_length=150)
    user_profile_picture = models.ImageField()
    body = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    magazine = models.ForeignKey(to=Magazine, on_delete=models.CASCADE, related_name="comments")
