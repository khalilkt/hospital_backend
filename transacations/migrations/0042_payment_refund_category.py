# Generated by Django 4.1.6 on 2024-01-14 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0041_remove_analyseaction_is_taazour_insurance'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='refund_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
