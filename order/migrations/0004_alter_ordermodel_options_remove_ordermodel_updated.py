# Generated by Django 5.0.7 on 2024-08-13 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_ordermodel_sent_ordermodel_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordermodel',
            options={'ordering': ('paid', '-created'), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='updated',
        ),
    ]