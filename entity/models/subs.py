from django.db import models 
from django.conf import settings
import datetime 
from django.db.models import F, CharField, Sum , When, Case, DecimalField, ExpressionWrapper, Subquery, OuterRef, Value, BooleanField
from rest_framework import serializers
from rest_framework.fields import empty
from transacations.models import TicketAction
from entity.models.hospital_tickets import TicketSerializer
from django.db.models.functions import Coalesce
from django.db.models import JSONField, Func, Value, CharField, IntegerField, When, Case, BooleanField, ExpressionWrapper, DateField, DateTimeField, DurationField

class ClientManager(models.Manager): 
    def with_status(self):
        sub = TicketAction.objects.filter(ticket__is_hospital_subscription = True, client = OuterRef("pk")).values('ticket').annotate(
             dur = Coalesce(F("duration"), Value(0)) * Case(
                When(ticket__duration_type = "4", then = Value(30)),
                When(ticket__duration_type = "5", then = Value(365)),
                default = Value(0),
                output_field = IntegerField()
            ),
            start_date_epoch = ExpressionWrapper(
        (F('created_at') - datetime.datetime(1970, 1, 1)) / 1_000_000,
        output_field=IntegerField()
    ),
            end_date_epoch = ExpressionWrapper(
            F('start_date_epoch') + (F("dur") * 24 * 60 * 60 ),
            output_field=IntegerField()
        ),
        ).order_by("-start_date_epoch")

        ret = self.annotate(
            # get last subscription
            last_sub = Subquery(sub.values('end_date_epoch')[:1]),
            is_active = Case(
                When(last_sub__isnull = True, then = Value(False)),
                When(last_sub__gte = datetime.datetime.now().timestamp(), then = Value(True)),
                default = Value(False),
                output_field = BooleanField()
            ),
            

        )

        return ret


class Client(models.Model):
    name = models.CharField(max_length=255)
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='clients')

    objects = ClientManager()

class ClientSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    tickets = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)   
    last_sub = serializers.IntegerField(read_only=True)
    def get_tickets(self, obj): 
        from transacations.models.ticket_action import TicketActionSerializer
        ret = obj.ticket_actions
        return TicketActionSerializer(ret, many=True).data



    class Meta:
        model = Client
        fields = "__all__"
