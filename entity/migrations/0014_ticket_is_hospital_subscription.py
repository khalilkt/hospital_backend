# Generated by Django 4.1.6 on 2023-12-26 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0013_client_hospital_show_in_subs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_hospital_subscription',
            field=models.BooleanField(default=False),
        ),
    ]
