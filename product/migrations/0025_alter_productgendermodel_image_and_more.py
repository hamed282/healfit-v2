# Generated by Django 5.0.7 on 2024-08-12 07:39

import upload_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_productcategorymodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productgendermodel',
            name='image',
            field=models.FileField(upload_to=upload_path.get_gender_upload_path),
        ),
        migrations.AlterField(
            model_name='productsubcategorymodel',
            name='image',
            field=models.FileField(upload_to=upload_path.get_subcategory_upload_path),
        ),
    ]