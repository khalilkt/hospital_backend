from django.db import models
from rest_framework import serializers
from entity.models.medicament import Medicament
from transacations.models.medicament_sale_item import MedicamentSaleItemSerializer, MedicamentSaleItem
from django.db import transaction

class MedicamentSale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicamentSaleSerializer(serializers.ModelSerializer):
    items = MedicamentSaleItemSerializer(many=True, read_only=False)
    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Items cannot be empty")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            items = validated_data.pop('items')
            medicament_sale = MedicamentSale.objects.create(**validated_data)

            for item in items:
                medicament = item['medicament']
                medicament.quantity -= item['quantity']
                medicament.save()
                MedicamentSaleItem.objects.create(parent=medicament_sale, **item)
                
            return medicament_sale


    class Meta:
        model = MedicamentSale
        fields = "__all__"
    

    