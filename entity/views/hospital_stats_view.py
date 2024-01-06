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
from django.db.models import Sum, Count, F, Q, Value, CharField, IntegerField, When, Case
from rest_framework import serializers
from django.db.models.functions import Concat, Coalesce


class StatsSerializer(serializers.Serializer):
    today_operations_count = serializers.IntegerField() 
    today_analyses_count = serializers.IntegerField() 
    today_medicaments_count = serializers.IntegerField()
    today_tickets_count = serializers.IntegerField()
    today_revenue = serializers.FloatField()
    month_revenue = serializers.FloatField()    
    year_revenue = serializers.FloatField()
    months_revenue = serializers.DictField()

class detailStatsSerializer(serializers.Serializer): 
    operations_count = serializers.IntegerField() 
    analyses_count = serializers.IntegerField() 
    medicaments_count = serializers.IntegerField()
    tickets_count = serializers.IntegerField()
    operations_revenue = serializers.FloatField()
    analyses_revenue = serializers.FloatField()
    medicaments_revenue = serializers.FloatField()
    tickets_revenue = serializers.FloatField()
    total_revenue = serializers.FloatField()

#  * 
#         Case(
#             When(Q(insurance_number__isnull = False) & Q(is_taazour_insurance = True), then = Value(0.0)),
#             When(Q(insurance_number__isnull = False) & Q(is_taazour_insurance = False), then = Value(0.1)),
#             When(insurance_number__isnull = True, then = Value(1.0)),
    #  default = Value(1),
    #     output_field = IntegerField()
    # )
    
def get_queryset(action, hospital_id = None):
    ret  = None
    if action== "operation" : 
        ret = OperationAction.objects
       
        ret = ret.annotate(revenue = F("payed_price"))
       
        if hospital_id: 
            ret = ret.filter(operation__hospital = hospital_id)
    elif action == "analyse":
        ret = AnalyseAction.objects
        ret  = ret.annotate(revenue = Sum(
            F("analyse_action_items__payed_price")
        ) )
        if hospital_id:
            ret = ret.filter(hospital = hospital_id)
    elif action == "medicament":
        ret = MedicamentSale.objects
        if hospital_id:
            ret = ret.filter(hospital = hospital_id)
        ret = ret.annotate(revenue = Sum(F("medicament_sale_items__payed_price")))
    elif action == "ticket":
        ret = TicketAction.objects
        ret = ret.annotate(revenue = F("payed_price"))
        if hospital_id:
            ret = ret.filter(ticket__hospital = hospital_id)
    
    else:
        raise serializers.ValidationError("Action not found : " + str(action) )  
    return ret

def get_stats_queryset_bymonthyear(action, hospital_id = None,  year = None, month = None, day = None):
    ret = get_queryset(action, hospital_id)
    if day:
        ret = ret.filter(created_at__day = str(day))
    if month:
        ret = ret.filter(created_at__month = str(month))
    if year:
        ret = ret.filter(created_at__year = str(year))
      
    ret = ret.values("revenue", "created_at").order_by("-created_at")
    return ret

def get_stats_queryset_bysDate_eDate(action, hospital_id = None,  sDate = None, eDate = None):
    ret = get_queryset(action, hospital_id)
    if sDate:
        ret = ret.filter(created_at__date__gte = sDate)
    if eDate:
        ret = ret.filter(created_at__date__lt = eDate)
      
    ret = ret.values("revenue", "created_at").order_by("-created_at")
    return ret

def get_range_date_revenue(hospital_id, sDate, eDate, include_hospital = False, include_pharmacy = False):
    if not include_hospital and not include_pharmacy:
        raise serializers.ValidationError("include_hospital or include_pharmacy must be true")
    
    if include_hospital:
        operations = get_stats_queryset_bysDate_eDate("operation", hospital_id, sDate, eDate)
        analyses = get_stats_queryset_bysDate_eDate("analyse", hospital_id, sDate, eDate)
        tickets = get_stats_queryset_bysDate_eDate("ticket", hospital_id, sDate, eDate)
    if include_pharmacy : 
        medicaments = get_stats_queryset_bysDate_eDate("medicament", hospital_id, sDate, eDate)
    range_revenue = 0
    if include_hospital:
        range_revenue += operations.aggregate(Sum('revenue'))["revenue__sum"] or 0
        range_revenue += analyses.aggregate(Sum('revenue') )['revenue__sum'] or 0
        range_revenue += tickets.aggregate(Sum('revenue'))['revenue__sum'] or 0
    if include_pharmacy:
        range_revenue += medicaments.aggregate(Sum('revenue'))['revenue__sum'] or 0
    return range_revenue

def get_range_revenue( hospital_id, year , month, ):
    operations = get_stats_queryset_bymonthyear("operation", hospital_id, year, month,)
    analyses = get_stats_queryset_bymonthyear("analyse", hospital_id, year, month,)
    medicaments = get_stats_queryset_bymonthyear("medicament", hospital_id, year, month,)
    tickets = get_stats_queryset_bymonthyear("ticket", hospital_id, year, month,)
    # subs = get_stats_queryset("subs", hospital_id, year, month,)

    month_revenue = operations.aggregate(Sum('revenue'))["revenue__sum"] or 0
    month_revenue += analyses.aggregate(Sum('revenue') )['revenue__sum'] or 0
    month_revenue += medicaments.aggregate(Sum('revenue'))['revenue__sum'] or 0
    month_revenue += tickets.aggregate(Sum('revenue'))['revenue__sum'] or 0
    # month_revenue += subs.aggregate(Sum('revenue'))['revenue__sum'] or 0
    return month_revenue
    

def get_sales_detail(hospital_id, year, month, day = None): 

    operations = get_stats_queryset_bymonthyear("operation", hospital_id, year, month,day)
    analyses = get_stats_queryset_bymonthyear("analyse", hospital_id, year, month, day)
    medicaments = get_stats_queryset_bymonthyear("medicament", hospital_id, year, month, day)
    tickets = get_stats_queryset_bymonthyear("ticket", hospital_id, year, month, day)
    # subs = get_stats_queryset("subs", hospital_id, year, month, day)

    operations_count = operations.count() 
    analyses_count = analyses.count()
    medicaments_count = medicaments.count()
    tickets_count = tickets.count()
    # subs_count = subs.count()
    # tickets_count += subs_count

    operations_revenue = operations.aggregate(Sum('revenue'))['revenue__sum'] or 0 
    analyses_revenue = analyses.aggregate(Sum('revenue'))['revenue__sum'] or 0 
    medicaments_revenue = medicaments.aggregate(Sum('revenue'))['revenue__sum'] or 0
    tickets_revenue = tickets.aggregate(Sum('revenue'))['revenue__sum'] or 0
    # subs_revenue = subs.aggregate(Sum('revenue'))['revenue__sum'] or 0

    # tickets_revenue += subs_revenue

    total_revenue =   operations_revenue + analyses_revenue + medicaments_revenue + tickets_revenue

    return { 
        "operations_count": operations_count,
        "analyses_count": analyses_count,
        "medicaments_count": medicaments_count,
        "tickets_count": tickets_count,
        "operations_revenue": operations_revenue,
        "analyses_revenue": analyses_revenue,
        "medicaments_revenue": medicaments_revenue,
        "tickets_revenue": tickets_revenue,
        "total_revenue" : total_revenue,
    } 




def get_response(hospital_id): 
    today = datetime.datetime.now().date()
    # today = today - datetime.timedelta(days=2)
    today_operations = get_stats_queryset_bymonthyear("operation", hospital_id, today.year, today.month, today.day)
    today_analyses = get_stats_queryset_bymonthyear("analyse", hospital_id, today.year, today.month, today.day)
    today_medicaments = get_stats_queryset_bymonthyear("medicament", hospital_id, today.year, today.month, today.day)
    today_tickets = get_stats_queryset_bymonthyear("ticket", hospital_id, today.year, today.month, today.day)
    # today_subs = get_stats_queryset("subs", hospital_id, today.year, today.month, today.day)

    today_revenue = today_operations.aggregate(Sum('revenue'))['revenue__sum'] or 0 
    today_revenue += today_analyses.aggregate(Sum('revenue'))['revenue__sum'] or 0
    today_revenue += today_medicaments.aggregate(Sum('revenue'))['revenue__sum'] or 0
    today_revenue += today_tickets.aggregate(Sum('revenue'))['revenue__sum'] or 0
    # today_revenue += today_subs.aggregate(Sum('revenue'))['revenue__sum'] or 0

    month_revenue = get_range_revenue(hospital_id, today.year, today.month)
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
    
class HospitalSalesStatsDetailView(APIView): 

    def get(self, request, hospital_id):
        params = request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)   
        if not year or not month : 
            return Response({"error": "year and month are required"}, status=400)
        sales_details = get_sales_detail(hospital_id, year, month, day) 
        return Response(detailStatsSerializer(sales_details).data)
        
class AdminSalesStatsDetailView(APIView):
    def get(self, request,):
        params = request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)   
        if not year or not month : 
            return Response({"error": "year and month are required"}, status=400)
        sales_details = get_sales_detail(None, year, month, day) 
        return Response(detailStatsSerializer(sales_details).data)
    
class AdminHospitalRenenueStatusView(APIView):
    def get(self, request,):

        params = request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)   
        if not year or not month : 
            return Response({"error": "year and month are required"}, status=400)
        hospitals = Hospital.objects.all()
        ret = {}
        for hospital in hospitals:
            name = hospital.name
            revenue = get_sales_detail(hospital.id, year, month, day)
            ret[name] = revenue["total_revenue"] - revenue["medicaments_revenue"]
            if hospital.has_pharmacy:
                ret[name + " (pharmacy)"] = revenue["medicaments_revenue"]
        return Response(ret)

            #  "operations_count": operations_count,
            # "analyses_count": analyses_count,
            # "medicaments_count": medicaments_count,
            # "tickets_count": tickets_count,
            # "operations_revenue": operations_revenue,
            # "analyses_revenue": analyses_revenue,
            # "medicaments_revenue": medicaments_revenue,
            # "tickets_revenue": tickets_revenue,
            # "total_revenue" : total_revenue,
        # hospital_id = params.get("hospital_id", None)
        # if hospital_id:
        #     hospital = Hospital.objects.get(id = hospital_id)
        #     if not hospital:
        #         return Response({"error": "hospital not found"}, status=400)
        # else:
        #     hospital = None
        # sDate = params.get("sDate", None)
        # eDate = params.get("eDate", None)
        # if sDate and eDate:
        #     sDate = datetime.datetime.strptime(sDate, "%Y-%m-%d").date()
        #     eDate = datetime.datetime.strptime(eDate, "%Y-%m-%d").date()
        #     if sDate > eDate:
        #         return Response({"error": "sDate must be less than eDate"}, status=400)
        # else:
        #     sDate = None
        #     eDate = None
        # include_hospital = params.get("include_hospital", None)
        # include_pharmacy = params.get("include_pharmacy", None)
        # if include_hospital == "true":
        #     include_hospital = True
        # else:
        #     include_hospital = False
        # if include_pharmacy == "true":
        #     include_pharmacy = True
        # else:
        #     include_pharmacy = False
        # if not include_hospital and not include_pharmacy:
        #     return Response({"error": "include_hospital or include_pharmacy must be true"}, status=400)
        # range_revenue = get_range_date_revenue(hospital_id, sDate, eDate, include_hospital, include_pharmacy)
        # return Response({"range_revenue": range_revenue})
        
        
class AdminHospitalStatsView(APIView):
     def get(self, request):
        return get_response(None)
