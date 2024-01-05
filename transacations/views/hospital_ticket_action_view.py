import datetime
from rest_framework.views import APIView
# from entity.models.subs import SubscriptionActionß
from transacations.models import TicketAction, TicketActionSerializer
from entity.models import Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from rest_framework import viewsets
from django.db.models import F, Value, CharField, IntegerField, Q, Sum, Count, When , Case, BooleanField, ExpressionWrapper, DateField, DateTimeField, DurationField
from django.db.models.functions import Concat, Coalesce, ExtractMonth, ExtractYear, ExtractDay
from django.db.models import JSONField, Func


from transacations.models.ticket_action import SubscriberSerializer
from transacations.views.utilis import get_queryset_by_date
# import Now()


class HospitalTicketsActionsView(ListCreateAPIView):
    serializer_class = TicketActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    

    ordering = ['-created_at']
    search_fields = ["ticket__name", "patient", "insurance_number",]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)  
        ret =  TicketAction.objects.filter(ticket__hospital = hospital_id)   
        ret = get_queryset_by_date(ret, year, month, day)
        return ret

    def get_paginated_response(self, data):
        ret =  super().get_paginated_response(data)
        ret.data["total"] = self.get_queryset().aggregate(total = Sum("payed_price"))["total"]
        return ret

class HospitalTicketActionsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketActionSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(TicketAction, ticket__hospital = hospital_id, id = id)  
        except TicketAction.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)


class Epoch(Func):
    function = 'strftime'
    template = '%s'
    output_field = IntegerField()


class HospitalSubscribersView(ListAPIView):
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-start_date']
    search_fields = ["patient", "insurance_number"]


    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        for_pirogue = self.request.query_params.get('for_pirogue', None)
        if status == "1":
            status = True
        elif status == "0":
            status = False
        else:
            status = None
        
        hospital_id = self.kwargs['hospital_id']
        ret = TicketAction.objects.filter(ticket__hospital= hospital_id)
        if not for_pirogue == "true":
            ret = ret.filter(ticket__is_subscription = True)
            
        ret = ret.annotate(
            start_date = F("created_at__date"),
            ticket_name = F("ticket__name"),
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
        duration_type = F("ticket__duration_type"),
        end_date_epoch = ExpressionWrapper(
            F('start_date_epoch') + (F("dur") * 24 * 60 * 60 ),
            output_field=IntegerField()
        ),
        status = Case(
            When(end_date_epoch__gte = datetime.datetime.now().timestamp(), then = Value(True)),
            default = Value(False),
            output_field = BooleanField()
        ),
        staff_name = F("created_by__name"), 
        client_name = Coalesce(F("client__name"), Value("")),
            
        )
        if status is not None: 
            ret = ret.filter(status = status)
        ret =ret.values("patient", "payload" , "start_date", "staff_name","id" , "ticket_name","start_date_epoch" ,"status", "end_date_epoch", "duration", "duration_type", "client_name" )

        return ret
