# Generated by Django 4.1.6 on 2024-01-25 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0030_municipaltaxdata_accounts'),
        ('transacations', '0042_payment_refund_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsurancePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('account', models.CharField(max_length=255)),
                ('quittance_number', models.CharField(max_length=255)),
                ('for_cnam', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_payments', to='entity.hospital')),
            ],
        ),
    ]
