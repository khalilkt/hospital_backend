from rest_framework.views import APIView
from transacations.models import OperationAction,  OperationActionSerializer
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

class HospitalOperationActionsView(ListCreateAPIView):
    serializer_class = OperationActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['-created_at']
    search_fields = ["operation__name", "patient", "insurance_number",]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)  
        ret =  OperationAction.objects.filter(operation__hospital = hospital_id)
        user_id = params.get("user", None)
        if user_id:
            ret = ret.filter(created_by = user_id)
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
        ret.data["total"] = self.get_queryset().aggregate(total = Sum("payed_price"))["total"]
        return ret
    
    
class HospitalOperationActionsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OperationActionSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(OperationAction, operation__hospital = hospital_id, id = id)  
        except OperationAction.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    