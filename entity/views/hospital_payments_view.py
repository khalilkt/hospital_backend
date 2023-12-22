from rest_framework.views import APIView
from transacations.models import Payment, PaymentSerializer
from entity.models import Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from rest_framework import viewsets

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated]

    ordering = ['id']
    search_fields = ['name']
    


class HospitalPaymentsView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['id']
    search_fields = ['name']
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return Payment.objects.filter(hospital = hospital_id)   

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
