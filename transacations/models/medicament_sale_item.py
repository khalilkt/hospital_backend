from django.db import models
from rest_framework import serializers

class MedicamentSaleItem(models.Model):
    parent = models.ForeignKey('MedicamentSale', on_delete=models.CASCADE, related_name='medicament_sale_items')
    medicament = models.ForeignKey('entity.Medicament', on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    # sale_price = models.FloatField()
    payed_price = models.DecimalField(max_digits=10, decimal_places=2, default= 999)


class MedicamentSaleItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='medicament.name', read_only=True)
    class Meta:
        model = MedicamentSaleItem
        fields = [ 'medicament', 'quantity', "payed_price", "name"]

    def validate(self, attrs):
        if attrs['quantity'] > attrs['medicament'].quantity:
            raise serializers.ValidationError("Quantity not available in stock")
        return attrs
