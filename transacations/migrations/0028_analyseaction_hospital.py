# Generated by Django 4.1.6 on 2024-01-03 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0018_remove_medicament_codebarres'),
        ('transacations', '0027_remove_analyseaction_analyse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyseaction',
            name='hospital',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='entity.hospital'),
            preserve_default=False,
        ),
    ]
