# Generated by Django 4.1.6 on 2023-12-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0011_ticket_required_payload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='duration_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
