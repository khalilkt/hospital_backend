# Generated by Django 4.1.6 on 2024-01-12 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0024_director_refund_municipaltaxdata_director_municipal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='amount',
            field=models.JSONField(),
        ),
        migrations.CreateModel(
            name='MunicipalTaxCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('municipal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='entity.municipaltaxdata')),
            ],
        ),
    ]
