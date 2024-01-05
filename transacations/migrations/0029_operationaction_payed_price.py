# Generated by Django 4.1.6 on 2024-01-04 14:04

from django.db import migrations, models


def set_initial_payed_price(apps, schema_editor):
    Operation = apps.get_model('transacations', 'operationaction')
    for obj in Operation.objects.all():
        if obj.insurance_number is None:
            obj.payed_price = obj.price
        else:
            obj.payed_price = obj.price * (0 if obj.is_taazour_insurance else 0.1 )
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0028_analyseaction_hospital'),
    ]
    

    operations = [
        migrations.AddField(
            model_name='operationaction',
            name='payed_price',
            field=models.DecimalField( decimal_places=2, max_digits=10, default=999),
        ),
        migrations.RunPython(set_initial_payed_price),
    ]
