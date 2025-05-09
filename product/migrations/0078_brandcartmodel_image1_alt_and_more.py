# Generated by Django 5.0.7 on 2025-04-29 05:38

import upload_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0077_brandpagemodel_image_alt'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandcartmodel',
            name='image1_alt',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brandcartmodel',
            name='image1',
            field=models.ImageField(upload_to=upload_path.get_brand_cart_upload_path),
        ),
        migrations.AlterField(
            model_name='brandcartmodel',
            name='image2',
            field=models.ImageField(upload_to=upload_path.get_brand_cart_upload_path),
        ),
        migrations.AlterField(
            model_name='brandcartmodel',
            name='image3',
            field=models.ImageField(upload_to=upload_path.get_brand_cart_upload_path),
        ),
    ]
