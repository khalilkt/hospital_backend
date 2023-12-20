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

class HospitalOperationActionsView(ListCreateAPIView):
    serializer_class = OperationActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['id']
    search_fields = []
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return OperationAction.objects.filter(operation__hospital = hospital_id)
    
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
    