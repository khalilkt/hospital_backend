from django.db import models
from rest_framework import serializers

from maur_hopitaux import settings


class MunicipalTaxData(models.Model):
    hospital = models.OneToOneField("Hospital", on_delete=models.CASCADE, related_name="municipal_tax_data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Director(models.Model): 
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    municipal = models.ForeignKey(MunicipalTaxData, on_delete=models.CASCADE, related_name="directors")

class DirectorSerializer(serializers.ModelSerializer):
    total_alimentation = serializers.SerializerMethodField()
    total_refund = serializers.SerializerMethodField()

    def get_total_alimentation(self, obj):
        return obj.alimentation_set.aggregate(models.Sum('amount'))["amount__sum"] or 0

    def get_total_refund(self, obj):
        refunds = obj.refund_set.all() 
        total = 0
        for refund in refunds:
            total += sum(refund.amount.values())
        
        return total

    class Meta:
        model = Director
        fields = "__all__"

class MunicipalTaxDataSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)
    class Meta:
        model = MunicipalTaxData
        fields = "__all__"



class Alimentation(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE) 
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='alimentations', on_delete=models.SET_NULL, null=True, blank=True)

class AlimentationSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source="director.name", read_only=True)
    staff_name      = serializers.CharField(source="created_by.username", read_only=True) 
    
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)
    
    class Meta:
        model = Alimentation
        fields = "__all__"

class Refund(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE) 
    # category_1 : amount1, category_2 : amount2, ... 
    amount = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='refunds', on_delete=models.SET_NULL, null=True, blank=True)

class RefundSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source="director.name", read_only=True)
    staff_name      = serializers.CharField(source="created_by.username", read_only=True) 
    
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

    
    class Meta:
        model = Refund
        fields = "__all__"

        

    def validate_amount(self,  value): 
        if type(value) != dict:
            raise serializers.ValidationError("Amount should be a dictionary")
        if not all([type(i) == int for i in value.values()]):
            raise serializers.ValidationError("Amount should be a dictionary with values of type int")

        if not all([i in value for i in ["category_1", "category_2", "category_3"]]):
            raise serializers.ValidationError("Amount should be a dictionary with keys category_1, category_2, category_3")
        if len(value) != 3:
            non_required_keys = [item for item in value.keys() if item not in ["category_1", "category_2", "category_3"]]
            raise serializers.ValidationError(f"Amount should be a dictionary with keys category_1, category_2, category_3, you have {non_required_keys} as extra keys")
        return value