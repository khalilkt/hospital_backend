# view for hospital stats

import datetime
from rest_framework.views import APIView
from entity.models import Hospital

# response 
from entity.models import Analyses,Medicament, Operations, Ticket

from transacations.models import AnalyseAction, MedicamentSale, OperationAction, TicketAction
from django.db.models import Value, CharField, IntegerField


from rest_framework.response import Response
from transacations.models.medicament_sale import MedicamentSale
from django.db.models import Sum, Count, F, Q
from rest_framework import serializers

class StatsSerializer(serializers.Serializer):
    today_operations_count = serializers.IntegerField() 
    today_analyses_count = serializers.IntegerField() 
    today_medicaments_count = serializers.IntegerField()
    today_tickets_count = serializers.IntegerField()
    today_revenue = serializers.FloatField()
    month_revenue = serializers.FloatField()    
    year_revenue = serializers.FloatField()
    months_revenue = serializers.DictField()
    

def get_stats_queryset(action, hospital_id = None,  year = None, month = None, day = None):
    ret  = None
    if action== "operation" : 
        ret = OperationAction.objects
        if hospital_id: 
            ret = ret.filter(operation__hospital = hospital_id)
    elif action == "analyse":
        ret = AnalyseAction.objects
        if hospital_id:
            ret = ret.filter(analyse__hospital = hospital_id)
    elif action == "medicament":
        ret = MedicamentSale.objects
        if hospital_id:
            ret = ret.filter(hospital = hospital_id)
        ret = ret.annotate(price = Sum(F("medicament_sale_items__sale_price") * F("medicament_sale_items__quantity")))
    elif action == "ticket":
        ret = TicketAction.objects
        if hospital_id:
            ret = ret.filter(ticket__hospital = hospital_id)
    else:
        raise serializers.ValidationError("Action not found : " + action )      

    if day:
        ret = ret.filter(created_at__day = str(day))
    if month:
        ret = ret.filter(created_at__month = str(month))
    if year:
        ret = ret.filter(created_at__year = str(year))
      
    ret = ret.values("price", "created_at").order_by("-created_at")
    return ret

def get_range_revenue( hospital_id, year , month):
    today_operations = get_stats_queryset("operation", hospital_id, year, month,)
    analyses = get_stats_queryset("analyse", hospital_id, year, month,)
    medicaments = get_stats_queryset("medicament", hospital_id, year, month,)
    tickets = get_stats_queryset("ticket", hospital_id, year, month,)

    month_revenue = today_operations.aggregate(Sum('price'))['price__sum'] or 0
    month_revenue += analyses.aggregate(Sum('price'))['price__sum'] or 0
    month_revenue += medicaments.aggregate(Sum('price'))['price__sum'] or 0
    month_revenue += tickets.aggregate(Sum('price'))['price__sum'] or 0
    return month_revenue
    

def get_response(hospital_id): 
    today = datetime.datetime.now().date()
    # today = today - datetime.timedelta(days=2)
    today_operations = get_stats_queryset("operation", hospital_id, today.year, today.month, today.day)
    today_analyses = get_stats_queryset("analyse", hospital_id, today.year, today.month, today.day)
    today_medicaments = get_stats_queryset("medicament", hospital_id, today.year, today.month, today.day)
    today_tickets = get_stats_queryset("ticket", hospital_id, today.year, today.month, today.day)

    today_revenue = today_operations.aggregate(Sum('price'))['price__sum'] or 0 
    today_revenue += today_analyses.aggregate(Sum('price'))['price__sum'] or 0
    today_revenue += today_medicaments.aggregate(Sum('price'))['price__sum'] or 0
    today_revenue += today_tickets.aggregate(Sum('price'))['price__sum'] or 0

    month_revenue = get_range_revenue(hospital_id, today.month, today.year)
    year_revenue = get_range_revenue(hospital_id, today.year,None)
        
    months_revenue = {}
    for i in range(1, 13):
        months_revenue[i] = get_range_revenue(hospital_id, today.year, i)
    
    return Response(StatsSerializer({
        "today_operations_count": today_operations.count(),
        "today_analyses_count": today_analyses.count(),
        "today_medicaments_count": today_medicaments.count(),
        "today_tickets_count": today_tickets.count(),
        "today_revenue": today_revenue,
        "month_revenue": month_revenue,
        "year_revenue": year_revenue,
        "months_revenue": months_revenue

    }).data)
    
class HospitalStatsView(APIView):
    def get(self, request, hospital_id):
        return get_response(hospital_id)
        
        
class AdminHospitalStatsView(APIView):
     def get(self, request):
        return get_response(None)