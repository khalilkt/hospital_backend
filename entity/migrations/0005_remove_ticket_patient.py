# Generated by Django 4.1.6 on 2023-12-18 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0004_alter_ticket_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='patient',
        ),
    ]
