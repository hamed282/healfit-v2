# Generated by Django 5.0.7 on 2024-09-12 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0045_productsubcategorymodel_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='cover_image_alt',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='description_image_alt',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='size_table_image_alt',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]