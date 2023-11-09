from django.db import models
from rest_framework import serializers

class MedicamentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default="")
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='medicament_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicamentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicamentCategory
        fields = "__all__"