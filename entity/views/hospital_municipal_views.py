from rest_framework.views import APIView
from entity.models import Director, DirectorSerializer , Hospital, Alimentation, AlimentationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import HopsitalPermission , IsHospitalDetailsAssignedUser
from entity.models.municipal_tax import Refund, RefundSerializer
from transacations.views.utilis import get_queryset_by_date
from django.db.models import Sum
from django.db.models.functions import Cast
from django.db import models


class HospitalDirectorsView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    
    ordering = ['name']
    search_fields = ['name', "phone_number"]

    def paginate_queryset(self, queryset):
        params = self.request.query_params 
        all = params.get("all", None)
        if all == "true":
            super().pagination_class.page_size = 1000
        else:
            super().pagination_class.page_size = 10
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']    
        return Director.objects.filter(municipal__hospital = hospital_id)
    
class HospitalDirectorsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Director, municipal__hospital = hospital_id, id = id)  
        except Director.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    
class MunicipalRefundView(ListCreateAPIView):
    serializer_class = RefundSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    
    ordering = ['-created_at']
    search_fields = ['director__name']

    def paginate_queryset(self, queryset):
        params = self.request.query_params 
        all = params.get("all", None)
        if all == "true":
            super().pagination_class.page_size = 1000
        else:
            super().pagination_class.page_size = 10
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)
        ret = Refund.objects.filter(director__municipal__hospital = hospital_id)
        user_id = params.get("user", None)
        if user_id:
            ret = ret.filter(created_by = user_id)
        ret = get_queryset_by_date(ret, year, month, day)
        return ret
    
    def get_paginated_response(self, data):
        ret = super().get_paginated_response(data)
        total =  self.get_queryset().aggregate(
            total_category_1 = Sum("amount__category_1", output_field=models.IntegerField()),
            total_category_2 = Sum("amount__category_2", output_field=models.IntegerField()),
            total_category_3 = Sum("amount__category_3", output_field=models.IntegerField())
            )
        ret.data["total"]= total
        return ret

class MunicipalRefundDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Refund, director__municipal__hospital = hospital_id, id = id)  
        except Refund.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class MunicipalAlimentationsView(ListCreateAPIView):
    serializer_class = AlimentationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    
    ordering = ['-created_at']
    search_fields = ['director__name']

    def paginate_queryset(self, queryset):
        params = self.request.query_params 
        all = params.get("all", None)
        if all == "true":
            super().pagination_class.page_size = 1000
        else:
            super().pagination_class.page_size = 10
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)
        ret = Alimentation.objects.filter(director__municipal__hospital = hospital_id)
        user_id = params.get("user", None)
        if user_id:
            ret = ret.filter(created_by = user_id)
        ret = get_queryset_by_date(ret, year, month, day)
        return ret

class MunicipalAlimentationsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AlimentationSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Alimentation, director__municipal__hospital = hospital_id, id = id)  
        except Alimentation.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)