from django.db import models
from rest_framework import serializers

class MedicamentSaleItem(models.Model):
    parent = models.ForeignKey('MedicamentSale', on_delete=models.CASCADE, related_name='medicament_sale_items')
    medicament = models.ForeignKey('entity.Medicament', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_price = models.FloatField()


class MedicamentSaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicamentSaleItem
        fields = "__all__"
    
    def validate(self, attrs):
        if attrs['quantity'] > attrs['medicament'].quantity:
            raise serializers.ValidationError("Quantity not available in stock")
        return attrs
