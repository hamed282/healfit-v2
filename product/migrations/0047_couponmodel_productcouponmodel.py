# Generated by Django 5.0.7 on 2024-09-14 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_alter_productmodel_cover_image_alt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('coupon', models.CharField(max_length=50, unique=True)),
                ('discount_percent', models.CharField(default=0, max_length=20)),
                ('discount_amount', models.CharField(default=0, max_length=20)),
                ('all_product', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('infinite', models.BooleanField(default=False)),
                ('limit', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expire', models.DateTimeField(blank=True, null=True)),
                ('extra_discount', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCouponModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.couponmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel')),
            ],
        ),
    ]