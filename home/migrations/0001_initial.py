# Generated by Django 5.0.7 on 2024-07-19 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerSliderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('banner', models.ImageField(upload_to='images/home/', verbose_name='image (1455*505 px)')),
            ],
            options={
                'verbose_name': 'Banner Slider',
                'verbose_name_plural': 'Banner Sliders',
            },
        ),
    ]