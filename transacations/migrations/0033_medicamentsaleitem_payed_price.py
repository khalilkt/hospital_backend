# Generated by Django 4.1.6 on 2024-01-04 14:57

from django.db import migrations, models

def set_initial_payed_price(apps, schema_editor):
    MedicamentSaleItem = apps.get_model('transacations', 'MedicamentSaleItem')
    for obj in MedicamentSaleItem.objects.all():
        if obj.parent.insurance_number is None:
            obj.payed_price = obj.sale_price * obj.quantity
        else:
            obj.payed_price = obj.sale_price *  obj.quantity * (0 if obj.parent.is_taazour_insurance else 0.1 )
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0032_auto_20240104_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamentsaleitem',
            name='payed_price',
            field=models.DecimalField(decimal_places=2, default=999, max_digits=10),
        ),
        migrations.RunPython(set_initial_payed_price),
    ]
