# Generated by Django 5.0.7 on 2025-06-06 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0098_alter_addimagegallerymodel_image_alt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategorymodel',
            name='banner_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productcategorymodel',
            name='banner_title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
