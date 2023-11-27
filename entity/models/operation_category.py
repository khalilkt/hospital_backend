from django.db import models
from rest_framework import serializers

class OperationCategory(models.Model):
    name = models.CharField(max_length=255, )
    description = models.TextField(default="")
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='operation_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OperationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = OperationCategory
        fields = "__all__"