from rest_framework.views import APIView
from entity.models import Operations, OperationsSerializer , Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters

class HospitalOperationsView(ListCreateAPIView):
    serializer_class = OperationsSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id']
    search_fields = ['name', 'category__name']

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return Operations.objects.filter(hospital = hospital_id)

class HospitalOperationsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OperationsSerializer

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Operations, hospital = hospital_id, id = id)  
        except Operations.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    