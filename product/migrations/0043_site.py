# Generated by Django 5.0.7 on 2024-09-11 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0042_alter_favusermodel_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
    ]
