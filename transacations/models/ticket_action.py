from django.db import models
from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import empty

class TicketAction(models.Model):
    ticket = models.ForeignKey('entity.Ticket', on_delete=models.CASCADE, related_name='actions')
    # today_id = models.IntegerField()
    duration = models.PositiveIntegerField(null = True, blank = True) # duratoin * duration_type
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ticket_actions', on_delete=models.SET_NULL, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    patient = models.CharField(max_length=255)

class TicketActionSerializer(serializers.ModelSerializer):
    
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = TicketAction
        fields = "__all__"