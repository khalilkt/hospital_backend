
from django.db import models
from django.conf import settings
from rest_framework import serializers 

class OperationAction(models.Model):
    operation = models.ForeignKey('entity.Operations', on_delete=models.CASCADE, related_name='actions')
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    # planned_date = models.DateTimeField()
    patient = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    doctor = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operation_actions', on_delete=models.SET_NULL, null=True, blank=True)

class OperationActionSerializer(serializers.ModelSerializer):
    operation_name = serializers.CharField(source='operation.name', read_only=True)
    staff_name = serializers.CharField(source='created_by.name', read_only=True)
    code= serializers.CharField(source='operation.code', read_only=True)
    
    class Meta:
        model = OperationAction
        fields = "__all__"
        extra_kwargs = {
            'created_by': {'required': True},
        }

    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)
