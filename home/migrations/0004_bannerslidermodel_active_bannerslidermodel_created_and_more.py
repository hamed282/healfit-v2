# Generated by Django 5.0.7 on 2024-07-22 13:26

import django.utils.timezone
from django.db import migrations, models


def create_default_video(apps, schema_editor):
    VideoHomeModel = apps.get_model('home', 'VideoHomeModel')
    VideoHomeModel.objects.create(video='input video')


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_commenthomemodel_active_commenthomemodel_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerslidermodel',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bannerslidermodel',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bannerslidermodel',
            name='banner',
            field=models.ImageField(upload_to='images/slide/', verbose_name='image (1455*505 px)'),
        ),
        migrations.RunPython(create_default_video),
    ]