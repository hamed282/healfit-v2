# Generated by Django 5.0.7 on 2025-03-17 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0068_productmodel_is_best_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyAreaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_area', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ClassNumberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_num', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_type', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='HearAboutUsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hear_about_us', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_category', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='CustomMadeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=32)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('body_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.bodyareamodel')),
                ('class_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.classnumbermodel')),
                ('customer_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.customertypemodel')),
                ('hear_about_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.hearaboutusmodel')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.producttypemodel')),
                ('treatment_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.treatmentcategorymodel')),
            ],
        ),
    ]
