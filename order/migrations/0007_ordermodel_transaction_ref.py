# Generated by Django 5.0.7 on 2024-09-07 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_rename_transaction_ref_ordermodel_ref_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='transaction_ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
