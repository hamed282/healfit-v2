# Generated by Django 5.0.7 on 2024-07-27 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_productmodel_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcategorymodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_product', to='product.productcategorymodel'),
        ),
        migrations.AlterField(
            model_name='addcategorymodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price',
            field=models.CharField(max_length=8),
        ),
    ]