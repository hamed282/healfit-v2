# Generated by Django 5.0.7 on 2025-04-30 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0080_productbrandmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbrandmodel',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
