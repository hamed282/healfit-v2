# Generated by Django 5.0.7 on 2025-04-30 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0078_brandcartmodel_image1_alt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='custommademodel',
            name='other_customer_type',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
