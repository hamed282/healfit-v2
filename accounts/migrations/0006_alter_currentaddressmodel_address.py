# Generated by Django 5.0.7 on 2024-07-18 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_currentaddressmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentaddressmodel',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.addressmodel'),
        ),
    ]
