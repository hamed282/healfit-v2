# Generated by Django 5.0.7 on 2024-09-16 05:58

import upload_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_blogmodel_banner_alter_blogmodel_banner_alt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='cover_image',
            field=models.ImageField(max_length=500, upload_to=upload_path.get_cover_blog_upload_path),
        ),
    ]