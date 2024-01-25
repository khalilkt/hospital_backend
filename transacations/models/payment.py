from django.db import models
from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import empty

class Payment(models.Model):
    amount = models.FloatField()
    payed_for = models.DateField()
    for_pharmacy = models.BooleanField()
    refund_category = models.CharField(max_length=255, null=True, blank=True)
    account = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    quittance_number = models.CharField(max_length=255)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='payments')
class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='created_by.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    start_date = serializers.DateField(read_only=True)

    def validate_payed_for(self, value):
        if value.weekday() != 1:
            raise serializers.ValidationError("Payment date should be a tuesday")
        return value    
    class Meta:
        model = Payment
        fields = "__all__"
    
class InsurancePayment(models.Model):
    amount = models.FloatField()
    account = models.CharField(max_length=255)
    quittance_number = models.CharField(max_length=255)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='insurance_payments')
    for_cnam = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    
class InsurancePaymentSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    class Meta:
        model = InsurancePayment
        fields = "__all__"

    