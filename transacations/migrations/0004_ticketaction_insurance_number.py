# Generated by Django 4.1.6 on 2023-12-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0003_payment_hospital_payment_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketaction',
            name='insurance_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
