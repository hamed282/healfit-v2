# Generated by Django 5.0.7 on 2024-09-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_addressmodel_prefix_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressmodel',
            name='iban_country',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]
