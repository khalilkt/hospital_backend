# Generated by Django 4.1.6 on 2023-12-19 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0006_hospital_created_at'),
        ('transacations', '0010_remove_operationaction_today_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyseAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today_id', models.IntegerField()),
                ('planned_date_time', models.DateTimeField()),
                ('insurance_number', models.CharField(max_length=255)),
                ('duration', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('analyse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='entity.analyses')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analyse_actions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
