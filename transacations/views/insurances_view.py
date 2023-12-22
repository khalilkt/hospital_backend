from rest_framework.generics import  ListAPIView, RetrieveAPIView
from transacations.models import OperationAction, AnalyseAction , MedicamentSale, TicketAction
from entity.models import Hospital
from django.db.models import F, CharField, Sum , DecimalField
from rest_framework import serializers
from django.db.models import Value
from django.db.models.functions import Concat, Coalesce
import datetime
from rest_framework.response import Response


class InssuranceSerializer(serializers.Serializer):
    name = serializers.CharField()
    insurance_number = serializers.CharField()
    price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    iid  = serializers.CharField() 

class InsuranceViews(ListAPIView):
    serializer_class = InssuranceSerializer
    def get_paginated_response(self, data):
        
        # ret.data['total'] = self.get_queryset().aggregate(total = Sum('price'))['total']
        ret =  super().get_paginated_response(data)
        return ret
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']

        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        operation_Q = OperationAction.objects.filter(insurance_number__isnull=False, operation__hospital= hospital_id)
        analyse_Q = AnalyseAction.objects.filter(insurance_number__isnull=False,analyse__hospital= hospital_id)
        medicament_Q = MedicamentSale.objects.filter(insurance_number__isnull=False, hospital= hospital_id)
        ticket_Q = TicketAction.objects.filter(insurance_number__isnull=False, ticket__hospital= hospital_id)

       
        if year:
            operation_Q = operation_Q.filter( created_at__year = year)
            analyse_Q = analyse_Q.filter(created_at__year = year)
            medicament_Q = medicament_Q.filter(created_at__year = year)
            ticket_Q = ticket_Q.filter(created_at__year = year)
        if year and month: 
            operation_Q = operation_Q.filter(created_at__month = month)
            analyse_Q = analyse_Q.filter(created_at__month = month)
            medicament_Q = medicament_Q.filter(created_at__month = month)
            ticket_Q = ticket_Q.filter(created_at__month = month)

        
        ret = operation_Q.annotate(name = F('operation__name'), iid = Concat(Value("op_"), F("id"), output_field=CharField())).union(
            analyse_Q.annotate(name = F('analyse__name'), iid = Concat(Value("an_"), F("id"), output_field=CharField()))
        ).union(
            medicament_Q.annotate( price = Sum(F("medicament_sale_items__sale_price") * F("medicament_sale_items__quantity")) , name = Value("Vente de medicament", output_field=CharField()), iid = Concat(Value("sl_"), F("id"), output_field=CharField()))
        ).union(
            ticket_Q.annotate(name = Value('Ticket Sale', output_field=CharField()), iid = Concat(Value("tk_"), F("id"), output_field=CharField()))
        ).values( 'name', 'created_at', 'insurance_number', 'price',"iid",).order_by('-created_at')
        
        return ret 
