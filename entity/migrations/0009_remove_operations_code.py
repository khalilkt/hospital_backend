# Generated by Django 4.1.6 on 2023-12-21 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0008_remove_analyses_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operations',
            name='code',
        ),
    ]
