from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

class Ticket(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField() #if has_duration is true then price is for 1 hour
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    # 1 = 30min, 2 = hours, 3 = days, 4 = months, 5 = years
    duration_type = models.CharField(max_length=255, null=True, blank=True)
    is_subscription = models.BooleanField(default=False)
    is_hospital_subscription = models.BooleanField(default=False) 
    required_payload = models.JSONField(default=dict, blank=True) 

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"