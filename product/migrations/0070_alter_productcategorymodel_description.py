# Generated by Django 5.0.7 on 2025-03-18 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0069_bodyareamodel_classnumbermodel_customertypemodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategorymodel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
