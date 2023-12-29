from django.db import models
from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import empty

class Payment(models.Model):
    amount = models.FloatField()
    payed_for = models.DateField()
    for_pharmacy = models.BooleanField()
    account = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    quittance_number = models.CharField(max_length=255)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='payments')

class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='created_by.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    start_date = serializers.DateField(read_only=True)

    def validate_payed_for(self, value):
        if value.weekday() != 0:
            raise serializers.ValidationError("Payment date should be a monday")
        return value    
    
    

    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            # 
            'created_by': {'required': True},
        }

    