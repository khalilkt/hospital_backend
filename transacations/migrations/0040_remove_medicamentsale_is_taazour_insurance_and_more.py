# Generated by Django 4.1.6 on 2024-01-07 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0039_medicamentsale_insurance_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicamentsale',
            name='is_taazour_insurance',
        ),
        migrations.RemoveField(
            model_name='operationaction',
            name='is_taazour_insurance',
        ),
        migrations.RemoveField(
            model_name='ticketaction',
            name='is_taazour_insurance',
        ),
    ]