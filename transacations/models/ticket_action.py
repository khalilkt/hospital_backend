from django.db import models
from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import empty
import datetime, time
from django.utils import timezone
from entity.models.hospital_tickets import TicketSerializer, Ticket
# from entity.models.subs import SubscriptionAction

class TicketAction(models.Model):
    ticket = models.ForeignKey('entity.Ticket', on_delete=models.CASCADE, related_name='actions')
    duration = models.PositiveIntegerField(null = True, blank = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_actions', on_delete=models.SET_NULL, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    patient = models.CharField(max_length=255, null=True, blank=True) 
    client = models.ForeignKey('entity.Client', on_delete=models.CASCADE, related_name='ticket_actions', null=True, blank=True)

    price = models.PositiveIntegerField()
    payload = models.JSONField(default=dict, blank=True) 



class TicketActionSerializer(serializers.ModelSerializer):
    ticket_name = serializers.CharField(source='ticket.name', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    duration_type = serializers.CharField(source='ticket.duration_type', read_only=True)
    staff_name = serializers.CharField(source='created_by.name', read_only=True)
    payload = serializers.JSONField(required=True)
    is_hospital_subscription = serializers.BooleanField(source='ticket.is_hospital_subscription', read_only=True)
    is_subscription = serializers.BooleanField(source='ticket.is_subscription', read_only=True)

    def validate_payload(self, value):
        ticket_id = self.initial_data.get("ticket", None)
        if not ticket_id:
            raise serializers.ValidationError("Ticket is required")
        try:
            ticket = Ticket.objects.get(id=ticket_id)   
            missing_keys = []     
            for key in ticket.required_payload:
                if key not in value:
                    missing_keys.append(key)
            if missing_keys:
                raise serializers.ValidationError(f"Missing keys: {missing_keys}")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Ticket does not exist")
        return value

    def validate(self, attrs):
        ticket_id = self.initial_data.get("ticket", None)
        if not ticket_id:
            raise serializers.ValidationError("Ticket is required")
        try:
            ticket = Ticket.objects.get(id=ticket_id)  
            patient = attrs.get("patient", None) 
            client = attrs.get("client", None) 

             
            is_subscription = ticket.is_subscription 
            if is_subscription and not client:
                raise serializers.ValidationError("Client is required")
            elif not is_subscription and not patient:
                raise serializers.ValidationError("Patient is required")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Ticket does not exist")

        return super().validate(attrs)
    
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
    ticket_name = serializers.CharField()
    start_date_epoch = serializers.IntegerField()
    end_date_epoch = serializers.IntegerField()
    start_date = serializers.DateField() 
    status = serializers.BooleanField()
    duration = serializers.IntegerField() 
    duration_type = serializers.CharField()
    staff_name = serializers.CharField()
    id = serializers.IntegerField()
    payload = serializers.JSONField()
    client_name = serializers.CharField()
 
    def to_representation(self, instance, ):
        ret = super().to_representation(instance) 
        ret["end_date"] = datetime.datetime.utcfromtimestamp(ret["end_date_epoch"] ).strftime("%Y-%m-%d")
        return ret

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)