# Generated by Django 4.1.6 on 2023-12-20 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0018_analyseaction_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyseaction',
            name='duration',
        ),
    ]