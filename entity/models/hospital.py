from django.db import models
from rest_framework import serializers
from entity.models.medicament import MedicamentSerializer

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    description = models.TextField()

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"