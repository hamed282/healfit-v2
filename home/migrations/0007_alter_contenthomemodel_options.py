# Generated by Django 5.0.7 on 2024-08-14 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_contenthomemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenthomemodel',
            options={'verbose_name': 'Content', 'verbose_name_plural': 'Content'},
        ),
    ]