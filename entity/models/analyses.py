from django.db import models
from rest_framework import serializers

from entity.models.analyse_categories import AnalyseCategory



class Analyses(models.Model): 
    name = models.CharField(max_length=255, )
    price = models.FloatField()
    code = models.CharField(max_length=255, )
    description = models.TextField(default="")
    category = models.ForeignKey('entity.AnalyseCategory', on_delete=models.CASCADE, related_name='analyses')
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='analyses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnalysesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyses
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'GET':
            fields['category'] = serializers.SlugRelatedField(slug_field='name', read_only=True)
        else:
            fields['category'] = serializers.CharField()
        return fields


    def create(self, validated_data):
        category = validated_data.pop('category')
        if len(category) <3:
            raise serializers.ValidationError("Category name must be at least 3 characters")
        
        category = AnalyseCategory.objects.get_or_create(name=category, hospital=validated_data['hospital'])[0]
    
        validated_data['category'] = category
        return super().create(validated_data)
    
    def update(self,instance, validated_data ):
        category = validated_data.pop('category' , None)
        if category is not None:
            if len(category) <3:
                raise serializers.ValidationError("Category name must be at least 3 characters")
            
            category = AnalyseCategory.objects.get_or_create(name=category, hospital=validated_data['hospital'])[0]
            validated_data['category'] = category

        return super().update(instance, validated_data)
    