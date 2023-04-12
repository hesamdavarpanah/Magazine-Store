# Generated by Django 4.1.6 on 2023-02-09 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='package/package_images')),
            ],
        ),
    ]