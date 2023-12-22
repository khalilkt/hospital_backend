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

class HospitalAnalysesActionsView(ListCreateAPIView):
    serializer_class = AnalyseActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['id']
    search_fields = ["analyse__name"]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return AnalyseAction.objects.filter(analyse__hospital = hospital_id)
    
class HospitalAnalysesActionsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnalyseActionSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(AnalyseAction, analyse__hospital = hospital_id, id = id)  
        except AnalyseAction.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)