from django.db import models
from rest_framework import serializers
from entity.models.medicament import Medicament
from transacations.models.medicament_sale_item import MedicamentSaleItemSerializer, MedicamentSaleItem
from django.db import transaction
from django.conf import settings

class MedicamentSale(models.Model):
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='medicaments_actions', on_delete=models.SET_NULL, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True) 
    patient = models.CharField(max_length=255)

class MedicamentSaleSerializer(serializers.ModelSerializer):

    items = MedicamentSaleItemSerializer(many=True, read_only=False, source = 'medicament_sale_items')
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)
    
    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Items cannot be empty")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            items = validated_data.pop('medicament_sale_items')
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
    

    