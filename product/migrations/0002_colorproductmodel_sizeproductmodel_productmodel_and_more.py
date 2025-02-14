# Generated by Django 5.0.7 on 2024-07-22 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=120)),
                ('color_code', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Color Product',
                'verbose_name_plural': 'Color Product',
            },
        ),
        migrations.CreateModel(
            name='SizeProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=120)),
                ('priority', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Size Product',
                'verbose_name_plural': 'Size Products',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='images/product/cover/')),
                ('size_table_image', models.ImageField(blank=True, null=True, upload_to='images/product/size_table/')),
                ('description_image', models.ImageField(blank=True, null=True, upload_to='images/product/description/')),
                ('price', models.IntegerField()),
                ('percent_discount', models.IntegerField(blank=True, null=True)),
                ('subtitle', models.CharField(max_length=256)),
                ('application_fields', models.TextField()),
                ('descriptions', models.TextField()),
                ('group_id', models.CharField(max_length=100)),
                ('priority', models.IntegerField(blank=True, default=1, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('follow', models.BooleanField(default=False)),
                ('index', models.BooleanField(default=False)),
                ('canonical', models.CharField(blank=True, max_length=256, null=True)),
                ('meta_title', models.CharField(max_length=60)),
                ('meta_description', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gender_product', to='product.productgendermodel')),
            ],
            options={
                'verbose_name': 'Item Groups',
                'verbose_name_plural': 'Item Groups',
            },
        ),
        migrations.CreateModel(
            name='PopularProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='popular_product', to='product.productmodel')),
            ],
            options={
                'verbose_name': 'Popular Product',
                'verbose_name_plural': 'Popular Products',
            },
        ),
        migrations.CreateModel(
            name='AddImageGalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/product/gallery/')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.colorproductmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_gallery_product', to='product.productmodel')),
            ],
            options={
                'verbose_name': 'Product Image Gallery',
                'verbose_name_plural': 'Product Image Gallery',
            },
        ),
        migrations.CreateModel(
            name='ProductVariantModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('item_id', models.CharField(max_length=100, verbose_name='Product ID')),
                ('price', models.IntegerField()),
                ('percent_discount', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_product', to='product.colorproductmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_color_size', to='product.productmodel')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_product', to='product.sizeproductmodel')),
            ],
            options={
                'verbose_name': 'Items',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.AddConstraint(
            model_name='productvariantmodel',
            constraint=models.UniqueConstraint(fields=('product', 'color', 'size'), name='unique_prod_color_size_combo'),
        ),
    ]
