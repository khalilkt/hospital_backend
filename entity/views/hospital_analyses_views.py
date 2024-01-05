from rest_framework.views import APIView
from entity.models import Analyses, AnalysesSerializer , Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import HopsitalPermission , IsHospitalDetailsAssignedUser

class HospitalAnalysesView(ListCreateAPIView):
    serializer_class = AnalysesSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    
    ordering = ['name']
    search_fields = ['name']
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
        return Analyses.objects.filter(hospital = hospital_id)

class HospitalAnalysesDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnalysesSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Analyses, hospital = hospital_id, id = id)  
        except Analyses.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    