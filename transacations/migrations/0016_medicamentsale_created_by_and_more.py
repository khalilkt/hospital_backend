# Generated by Django 4.1.6 on 2023-12-20 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0007_remove_medicamentcategory_hospital_and_more'),
        ('transacations', '0015_remove_analyseaction_planned_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamentsale',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medicaments_actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicamentsale',
            name='insurance_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='medicamentsale',
            name='patient',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='analyseaction',
            name='analyse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='actions', to='entity.analyses'),
        ),
    ]
