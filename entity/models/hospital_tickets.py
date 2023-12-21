from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

class Ticket(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField() #if has_duration is true then price is for 1 hour
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    # 1 = 30min, 2 = hours, 3 = days
    duration_type = models.SmallIntegerField(max_length=255, null=True, blank=True, )

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"