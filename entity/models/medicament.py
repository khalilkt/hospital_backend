from django.db import models
from rest_framework import serializers
from entity.models.medicament_category import MedicamentCategory

class Medicament(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='medicament')
    quantity = models.IntegerField()
    category = models.ForeignKey('entity.MedicamentCategory', on_delete=models.CASCADE, related_name='medicaments', null=True)
    codebarres = models.CharField(max_length=255, default="AQBBABABQB")    
    # image = models.ImageField(upload_to='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicamentSerializer(serializers.ModelSerializer):

    def get_fields(self):
        # if read category should be slug related field 
        # if write category should be just a string
        fields = super().get_fields()
        if self.context['request'].method == 'GET':
            fields['category'] = serializers.SlugRelatedField(slug_field='name', read_only=True)
        else:
            fields['category'] = serializers.CharField()
        return fields
    
    class Meta:
        model = Medicament
        fields = "__all__"  
    
    
    def create(self, validated_data):
        category = validated_data.pop('category')
        if len(category) <3:
            raise serializers.ValidationError("Category name must be at least 3 characters")
        
        category = MedicamentCategory.objects.get_or_create(name=category, hospital=validated_data['hospital'])[0]
    
        validated_data['category'] = category
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category = validated_data.pop('category', None )
        if category is not None:
            if len(category) <3:
                raise serializers.ValidationError("Category name must be at least 3 characters")
            category = MedicamentCategory.objects.get_or_create(name=category, hospital=validated_data['hospital'])[0]
            validated_data['category'] = category
        return super().update(instance,validated_data)