from rest_framework.views import APIView
from transacations.models import AnalyseAction, AnalyseActionSerializer
from entity.models import Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from rest_framework import viewsets
from django.db.models import F, Value, CharField, IntegerField, Q, Sum, Count, When , Case, BooleanField, ExpressionWrapper, DateField, DateTimeField, DurationField

from transacations.views.utilis import get_queryset_by_date

class HospitalAnalysesActionsView(ListCreateAPIView):
    serializer_class = AnalyseActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['-created_at']
    search_fields = [ "patient", "insurance_number", "analyse_action_items__analyse__name"]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)   
        ret = AnalyseAction.objects.filter(hospital = hospital_id)
        ret = get_queryset_by_date(ret, year, month, day)
        return ret
    
    def paginate_queryset(self, queryset):
        params = self.request.query_params 
        all = params.get("all", None)
        if all == "true":
            super().pagination_class.page_size = 1000
        else:
            super().pagination_class.page_size = 10
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        ret =  super().get_paginated_response(data)
        ret.data["total"] = self.get_queryset().aggregate(total = Sum("analyse_action_items__payed_price"))["total"]
        return ret
    
class HospitalAnalysesActionsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnalyseActionSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(AnalyseAction,hospital = hospital_id, id = id)  
        except AnalyseAction.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)