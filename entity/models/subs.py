from django.db import models 
from django.conf import settings
import datetime 
from django.db.models import F, CharField, Sum , When, Case, DecimalField, ExpressionWrapper, Subquery, OuterRef, Value, BooleanField
from rest_framework import serializers
from rest_framework.fields import empty

class ClientManager(models.Manager): 
    def with_status(self):
        last_sub  = Subquery(self.model.objects.filter(id=OuterRef('id')).order_by('-subscriptions__created_at').values('subscriptions__created_at')[:1])
        return self.annotate(
            # end_date = last_sun__created_at + 365 days
            end_date = ExpressionWrapper(
                last_sub + datetime.timedelta(days=365),
                output_field=models.DateTimeField()
            ),
          
            status = 
                Case(
                    When(end_date__gte = datetime.datetime.now(), then = Value(True)),
                    default = Value(False),
                    output_field = BooleanField()
                )
               
            

        )


class Client(models.Model):
    name = models.CharField(max_length=255)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='clients')

    objects = ClientManager()

class ClientSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    

    class Meta:
        model = Client
        fields = "__all__"

class SubscriptionAction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscription_actions', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    

class SubscriptionActionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    staff_name = serializers.CharField(source='created_by.name', read_only=True)

    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = SubscriptionAction
        fields = "__all__"