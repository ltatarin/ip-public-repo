# Generated by Django 4.2.10 on 2024-06-26 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nasa_image_gallery', '0002_alter_favourite_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourite',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]