# Generated by Django 4.1.6 on 2023-02-09 23:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150)),
                ('body', models.TextField()),
                ('instagram_link', models.URLField()),
                ('telegram_link', models.URLField()),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='article/article_images')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('user_profile_picture', models.ImageField(null=True, upload_to='')),
                ('body', models.TextField()),
                ('rate', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.article')),
            ],
        ),
    ]