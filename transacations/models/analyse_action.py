
from django.db import models
from django.conf import settings
from rest_framework import serializers
from django.db import transaction
from transacations.models.constants import INSURANCE_CHOICES

class AnalyseAction(models.Model):
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    insurance_name = models.CharField(max_length=255, null=True, blank=True, choices=INSURANCE_CHOICES)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE)
    patient  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='analyse_actions', on_delete=models.SET_NULL, null=True, blank=True)

class AnalyseActionItem(models.Model):
    parent = models.ForeignKey('AnalyseAction', on_delete=models.CASCADE, related_name='analyse_action_items')
    analyse = models.ForeignKey('entity.Analyses', on_delete=models.CASCADE, related_name='analyse_actions')
    # price = models.FloatField() 
    payed_price = models.DecimalField(max_digits=10, decimal_places=2)

class AnalyseActionItemSerializer(serializers.ModelSerializer):
    analyse_name = serializers.CharField(source='analyse.name', read_only=True) 
    class Meta:
        model = AnalyseActionItem
        fields = [ 'analyse', 'analyse_name', "payed_price"]

class AnalyseActionSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='created_by.name', read_only=True)
    items = AnalyseActionItemSerializer(many=True, read_only=False, source = 'analyse_action_items')
    total = serializers.SerializerMethodField() 
    def get_total(self, obj):
        return sum([item['payed_price'] for item in obj.analyse_action_items.values('payed_price')])
    
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

        
    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Items cannot be empty")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            items = validated_data.pop('analyse_action_items')
            analyse_action = AnalyseAction.objects.create(**validated_data)
            for item in items:
                AnalyseActionItem.objects.create(parent=analyse_action, **item)
            return analyse_action

    class Meta:
        model = AnalyseAction
        fields = "__all__"
        extra_kwargs = {
            'created_by': {'required': True},
        }