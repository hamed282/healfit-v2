# Generated by Django 5.0.7 on 2024-09-14 11:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_couponmodel_productcouponmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='couponmodel',
            old_name='coupon',
            new_name='coupon_code',
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]