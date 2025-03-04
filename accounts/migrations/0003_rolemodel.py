# Generated by Django 5.0.7 on 2024-07-13 12:09
from django.db import migrations, models


def create_default_role(apps, schema_editor):
    RoleModel = apps.get_model('accounts', 'RoleModel')
    RoleModel.objects.create(role='user')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_addressmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=32)),
            ],
        ),
        migrations.RunPython(create_default_role),
    ]
