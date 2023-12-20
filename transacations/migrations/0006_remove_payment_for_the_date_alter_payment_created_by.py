# Generated by Django 4.1.6 on 2023-12-18 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transacations', '0005_ticketaction_patient_alter_payment_quittance_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='for_the_date',
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
    ]
