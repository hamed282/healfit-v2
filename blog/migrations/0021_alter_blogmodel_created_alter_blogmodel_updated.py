# Generated by Django 5.0.7 on 2025-02-24 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_blogmodel_author_image_blogmodel_read_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
