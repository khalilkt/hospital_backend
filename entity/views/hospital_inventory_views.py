from rest_framework.views import APIView
from entity.models import Hospital, Medicament, MedicamentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters

class HospitalInventoryView(ListCreateAPIView):
    serializer_class = MedicamentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id']
    search_fields = ['name', 'category__name', "codebarres"]

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return Medicament.objects.filter(hospital = hospital_id)        
    
    
class HospitalInventoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicamentSerializer

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Medicament, hospital = hospital_id, id = id)  
        except Medicament.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    