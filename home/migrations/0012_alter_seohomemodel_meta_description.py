# Generated by Django 5.0.7 on 2024-08-30 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_logomodel_logo_alt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seohomemodel',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
