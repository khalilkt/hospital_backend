from rest_framework.views import APIView
from entity.models.municipal_tax import MunicipalTaxData
from entity.views.hospital_stats_view import get_range_date_revenue, get_range_taxrefunds_revenue, get_stats_queryset_bysDate_eDate
from maur_hopitaux.pagination import MPagePagination
from transacations.models import Payment, PaymentSerializer, InsurancePayment, InsurancePaymentSerializer
from entity.models import Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from rest_framework import viewsets, serializers
import datetime
from django.db.models import F, Value, CharField, IntegerField, Q, Sum, Count, When , Case, BooleanField, ExpressionWrapper, DateField, DateTimeField, DurationField
from django.db.models.functions import Concat, Coalesce, Cast, TruncDate
from django.db.models import OuterRef, Subquery
from django.db.models import FloatField
from transacations.views.insurances_view import def_insurance_query



def get_payment_queryset(hospital_id, for_pharmacy):
    if not for_pharmacy:
        for_pharmacy = False
    
    ret = Payment.objects.filter(hospital = hospital_id, for_pharmacy = for_pharmacy)

    ret = ret.annotate(
        start_date_temp = F('payed_for') - datetime.timedelta(days = 7),
        start_date = Case(
            When(start_date_temp__lt = F("hospital__created_at__date"), then = F("hospital__created_at__date")),
            default = F('start_date_temp'),
            output_field = DateField(),
        ),
    )
    ret = ret.order_by('-payed_for')
    return ret

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, ):
        hospital_id = self.kwargs['hospital_id']
        for_pharmacy = self.request.query_params.get('for_pharmacy', False)
        ret = get_payment_queryset(hospital_id, for_pharmacy)
        return ret

    ordering = ['id']
    search_fields = ['name']

class HospitalPaymentsView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['-created_at']
    search_fields = ['hospital__name', "account", "quittance_number","amount" ]
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
        for_pharmacy = self.request.query_params.get('for_pharmacy', False)

        return get_payment_queryset(hospital_id, for_pharmacy)
  


class HospitalPaymentsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Payment, hospital = hospital_id, id = id)  
        except Payment.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
  
class HopsitalInsurancePaymentsView(ListCreateAPIView):
    serializer_class = InsurancePaymentSerializer 
    filter_backends = [filters.OrderingFilter, filters.SearchFilter] 
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    ordering = ['-created_at']
    search_fields = ['hospital__name', "account", "quittance_number","amount"]

    def paginate_queryset(self, queryset):
            params = self.request.query_params 
            all = params.get("all", None)
            if all == "true":
                super().pagination_class.page_size = 1000
            else:
                super().pagination_class.page_size = 10
            return super().paginate_queryset(queryset)
    
    def get_paginated_response(self, data):
        ret = super().get_paginated_response(data)
        q = self.get_queryset()
        ret.data["total"] = q.aggregate(total = Sum("amount"))["total"] or 0
        for_cnam = self.request.query_params.get('for_cnam', None)
        insurances = "[CNAM, TAAZOUR]" if for_cnam == "True" else "[HILAL]"
        total_refunded_by_insurance = def_insurance_query(hospital_id= self.kwargs['hospital_id'], insurances=insurances).aggregate(total_revenue =ExpressionWrapper(Sum(ExpressionWrapper( F("normal_price")- F("revenue"), output_field=FloatField())) , output_field=FloatField(), ))["total_revenue"] or 0
        ret.data["rest"] =  total_refunded_by_insurance - ret.data["total"]
        return ret

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        for_cnam = self.request.query_params.get('for_cnam', None)
        if not for_cnam:
            raise serializers.ValidationError("for_cnam is required")
        return InsurancePayment.objects.filter(hospital = hospital_id, for_cnam = for_cnam)
    
class HospitalInsurancePaymentsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = InsurancePaymentSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(InsurancePayment, hospital = hospital_id, id = id)  
        except InsurancePayment.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
class WeekPaymentSerializer(serializers.Serializer):
    date = serializers.DateField()
    start = serializers.DateField()
    end = serializers.DateField()
    revenue = serializers.IntegerField()

class HopsitalNotPayedView(APIView):
    serializer_class = WeekPaymentSerializer

    def get(self, request, hospital_id):
        for_pharmacy = self.request.query_params.get('for_pharmacy', False)
        refund_category = self.request.query_params.get('refund_category', None)
        if for_pharmacy:
            if for_pharmacy == "True":
                for_pharmacy = True
            else:
                for_pharmacy = False
        hospital = get_object_or_404(Hospital, id = hospital_id)
        if MunicipalTaxData.objects.filter(hospital = hospital_id).exists() and refund_category is None:
            return Response(status = status.HTTP_400_BAD_REQUEST, data = {
                "error" : "refund_category is required for municipal tax hospital"
            })
        payments = Payment.objects.filter(hospital = hospital_id, for_pharmacy = for_pharmacy)
        if refund_category: 
            payments = payments.filter(refund_category = refund_category)
        date = hospital.created_at.date()
        # every tuesday
        while date.weekday() != 1:
            date = date + datetime.timedelta(days = 1)
        
            
        ret = []
        if date == hospital.created_at.date():
            date = date + datetime.timedelta(days = 7)
        while date <= (datetime.datetime.now().date()):
            start_date = date - datetime.timedelta(days = 7)
            if start_date <= hospital.created_at.date():
                start_date = hospital.created_at.date()
            week_payments = payments.filter(payed_for = date)
            # end date is exluded
            if not week_payments.exists():
                if refund_category : 
                    revenue = get_range_taxrefunds_revenue(hospital_id, start_date, date, refund_category = refund_category)
                else:
                    revenue = get_range_date_revenue(hospital_id, start_date, date, include_hospital=  not for_pharmacy , include_pharmacy= for_pharmacy)
                ret.append({
                    "date" : date,
                    "start" : start_date,
                    "end" : date,
                    "revenue" : revenue,
                })
            date = date + datetime.timedelta(days = 7)

        paginator = MPagePagination()
        page = paginator.paginate_queryset(ret, request)
        serializer = WeekPaymentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)