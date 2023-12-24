import datetime
from rest_framework.views import APIView
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
from django.db.models import Func


from transacations.models.ticket_action import SubscriberSerializer
# import Now()


class HospitalTicketsActionsView(ListCreateAPIView):
    serializer_class = TicketActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['-created_at']
    search_fields = ["ticket__name", "patient", "insurance_number",]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return TicketAction.objects.filter(ticket__hospital = hospital_id)   

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
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-start_date']
    search_fields = ["patient", "insurance_number"]


    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status == "1":
            status = True
        elif status == "0":
            status = False
        else:
            status = None
        
        hospital_id = self.kwargs['hospital_id']
        ret = TicketAction.objects.filter(ticket__hospital= hospital_id, ticket__is_subscription = True)
        ret = ret.annotate(
            start_date = F("created_at__date"),
            ticket_name = F("ticket__name"),
            dur = Coalesce(F("duration"), Value(0)) * Case(
                When(ticket__duration_type = 4, then = Value(30)),
                When(ticket__duration_type = 5, then = Value(365)),
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
                When(end_date_epoch__gte = datetime.datetime(2024,1,24).timestamp(), then = Value(True)),
                default = Value(False),
                output_field = BooleanField()
            ),
            staff_name = F("created_by__name"), 
            
        )
        if status is not None: 
            ret = ret.filter(status = status)
        ret =ret.values("patient", "start_date", "dur", "staff_name","id" , "ticket_name","start_date_epoch" ,"status", "end_date_epoch", "duration", "duration_type" )

        return ret
