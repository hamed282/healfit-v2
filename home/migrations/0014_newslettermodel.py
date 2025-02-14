# Generated by Django 5.0.7 on 2024-09-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_bannerslidermodel_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'NewsLetter',
                'verbose_name_plural': 'NewsLetter',
            },
        ),
    ]
