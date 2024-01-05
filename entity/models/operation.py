from django.db import models
from rest_framework import serializers

class Operations(models.Model): 
    name = models.CharField(max_length=255, )
    price = models.FloatField()
    insurance_price = models.FloatField(null=True, blank=True)

    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='operations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = "__all__"
