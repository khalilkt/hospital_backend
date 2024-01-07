from rest_framework.generics import  ListAPIView, RetrieveAPIView
from transacations.models import OperationAction, AnalyseAction , MedicamentSale, TicketAction
from entity.models import Hospital
from django.db.models import F, CharField, Sum , DecimalField
from rest_framework import serializers
from django.db.models import Value
from django.db.models.functions import Concat, Coalesce
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import When, Case, FloatField , F, Q, ExpressionWrapper
from rest_framework.permissions import IsAuthenticated

class InssuranceSerializer(serializers.Serializer):
    name = serializers.CharField()
    insurance_number = serializers.CharField()
    insurance_name = serializers.CharField()
    revenue = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    iid  = serializers.CharField() 
    normal_price = serializers.IntegerField()

def def_query(hospital_id, insurances : str, year = None , month = None):

    insurances = insurances.upper().replace(" ", "").replace("[", "").replace("]" , "").split(",")
    operation_Q = OperationAction.objects.filter(insurance_number__isnull=False, insurance_name__in = insurances,   operation__hospital= hospital_id)
    analyse_Q = AnalyseAction.objects.filter(insurance_number__isnull=False,insurance_name__in = insurances,hospital= hospital_id)
    medicament_Q = MedicamentSale.objects.filter(insurance_number__isnull=False,insurance_name__in = insurances, hospital= hospital_id)
    ticket_Q = TicketAction.objects.filter(insurance_number__isnull=False,insurance_name__in = insurances, ticket__hospital= hospital_id)
    if year:
        operation_Q = operation_Q.filter( created_at__year = year)
        analyse_Q = analyse_Q.filter(created_at__year = year)
        medicament_Q = medicament_Q.filter(created_at__year = year)
        ticket_Q = ticket_Q.filter(created_at__year = year)
    if month: 
        operation_Q = operation_Q.filter(created_at__month = month)
        analyse_Q = analyse_Q.filter(created_at__month = month)
        medicament_Q = medicament_Q.filter(created_at__month = month)
        ticket_Q = ticket_Q.filter(created_at__month = month)
    
    ret = operation_Q.annotate(name = F('operation__name'), iid = Concat(Value("op_"), F("id"), output_field=CharField()), revenue=F("payed_price"), normal_price = Coalesce(F("operation__insurance_price"), F("operation__price"))).union(
     ).union(
        analyse_Q.annotate(name = Value("analyse"), iid = Concat(Value("an_"), F("id"), output_field=CharField()), revenue=   Sum(
            F("analyse_action_items__payed_price")
        ), normal_price = Sum(Coalesce(F("analyse_action_items__analyse__insurance_price"), F("analyse_action_items__analyse__price"))) )
    ).union(
        medicament_Q.annotate( name = Value("Vente de medicament", output_field=CharField()),iid = Concat(Value("sl_"), F("id"), output_field=CharField()), revenue = Sum(F("medicament_sale_items__payed_price")),
                              normal_price = Sum(F("medicament_sale_items__medicament__price") * F("medicament_sale_items__quantity"))
                              
    
    )
    ).union(
        ticket_Q.annotate(name = F("ticket__name"), iid = Concat(Value("tk_"), F("id"), output_field=CharField()), revenue  = F("payed_price") , normal_price = Coalesce(F("ticket__insurance_price"),F("ticket__price")) * Coalesce( F("duration"), Value(1)))
    ).values('name', 'created_at', 'insurance_number', "insurance_name","iid","revenue" , "normal_price").order_by('-created_at')
    return ret

# class TotalInsuranceView(APIView):
#     def get(self, request, hospital_id):
#         year = self.request.query_params.get('year', None)
#         month = self.request.query_params.get('month', None)
#         insurances = self.request.query_params.get('insurances', "")
#         ret = def_query(hospital_id, insurances, year, month)

#         ret = ret.aggregate(total_revenue =ExpressionWrapper( Sum("revenue") , output_field=FloatField()))
#         return Response(ret)

class InsuranceViews(ListAPIView):
    serializer_class = InssuranceSerializer
    def get_paginated_response(self, data):
        ret =  super().get_paginated_response(data)
        return ret
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        insurances = self.request.query_params.get('insurances', "")

        ret = def_query(hospital_id, insurances, year, month)

       
        return ret 

    def get_paginated_response(self, data):
        query = self.get_queryset()
        ret = super().get_paginated_response(data)
        ret.data["total"] = query.aggregate(total_revenue =ExpressionWrapper( Sum(ExpressionWrapper(F("revenue") - F("normal_price"))) , output_field=FloatField(), ))["total_revenue"]
        return ret