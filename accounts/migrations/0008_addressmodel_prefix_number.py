# Generated by Django 5.0.7 on 2024-09-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_addressmodel_emirats'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressmodel',
            name='prefix_number',
            field=models.CharField(default=1, max_length=8),
            preserve_default=False,
        ),
    ]
