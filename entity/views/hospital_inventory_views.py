from rest_framework.views import APIView
from entity.models import Hospital, Medicament, MedicamentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalAssignedUser , IsHospitalDetailsAssignedUser

class HospitalInventoryView(ListCreateAPIView):
    serializer_class = MedicamentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser]
    ordering = ['id']
    search_fields = ['name', 'category__name', "codebarres"]

    def get_serializer_context(self):
        hospital_id = self.kwargs['hospital_id']    
        context =  super().get_serializer_context()
        context['hospital_id'] = hospital_id
        return context

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return Medicament.objects.filter(hospital = hospital_id)

class HospitalInventoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicamentSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser ]
    

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Medicament, hospital = hospital_id, id = id)  
        except Medicament.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)