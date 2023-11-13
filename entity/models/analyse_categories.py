from django.db import models    
from rest_framework import serializers

class AnalyseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default="")
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='analyses_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnalyseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyseCategory
        fields = "__all__"