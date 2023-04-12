from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Article(models.Model):
    subject = models.CharField(max_length=150)
    body = models.TextField()
    instagram_link = models.URLField()
    telegram_link = models.URLField()
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="article/article_images")


class Comment(models.Model):
    username = models.CharField(max_length=150)
    user_profile_picture = models.ImageField(null=True)
    body = models.TextField()
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    publish_date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
