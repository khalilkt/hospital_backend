from django.db import models
from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import empty
import datetime, time
from django.utils import timezone

class TicketAction(models.Model):
    ticket = models.ForeignKey('entity.Ticket', on_delete=models.CASCADE, related_name='actions')
    duration = models.PositiveIntegerField(null = True, blank = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_actions', on_delete=models.SET_NULL, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    patient = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

class TicketActionSerializer(serializers.ModelSerializer):
    ticket_name = serializers.CharField(source='ticket.name', read_only=True)
    duration_type = serializers.CharField(source='ticket.duration_type', read_only=True)
    staff_name = serializers.CharField(source='created_by.name', read_only=True)
    
    
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = TicketAction
        fields = "__all__"

class SubscriberSerializer(serializers.Serializer):
    patient = serializers.CharField() 
    dur = serializers.IntegerField() 
    ticket_name = serializers.CharField()
    start_date_epoch = serializers.IntegerField()
    end_date_epoch = serializers.IntegerField()
    start_date = serializers.DateField() 
    status = serializers.BooleanField()
    duration = serializers.IntegerField() 
    duration_type = serializers.IntegerField()
    staff_name = serializers.CharField()
    id = serializers.IntegerField()
 
    def to_representation(self, instance, ):
        ret = super().to_representation(instance) 
        ret["end_date"] = datetime.datetime.utcfromtimestamp(ret["end_date_epoch"] ).strftime("%Y-%m-%d")
        return ret

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)