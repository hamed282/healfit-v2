# Generated by Django 5.0.7 on 2024-08-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_alter_addimagegallerymodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addimagegallerymodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/product/gallery/'),
        ),
    ]
