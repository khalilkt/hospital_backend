from django.db import models
from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import empty

class Payment(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    # for_the_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', on_delete=models.SET_NULL, null=True, blank=True)
    quittance_number = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=None, null=True, blank=True)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='payments')

class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='created_by.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)


    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            # 
            'created_by': {'required': True},
        }

    