# Generated by Django 4.1.6 on 2023-12-28 15:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0022_ticketaction_client_alter_ticketaction_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_valid',
        ),
        migrations.AddField(
            model_name='payment',
            name='payed_for',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
