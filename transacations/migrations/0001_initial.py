# Generated by Django 4.1.6 on 2023-12-15 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicamentSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='MedicamentSaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('sale_price', models.FloatField()),
                ('medicament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.medicament')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicament_sale_items', to='transacations.medicamentsale')),
            ],
        ),
    ]
