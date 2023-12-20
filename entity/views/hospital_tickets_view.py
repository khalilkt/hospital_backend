
from rest_framework.views import APIView
from entity.models import Ticket, TicketSerializer , Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser

class HospitalTicketView(ListCreateAPIView):
    serializer_class = TicketSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['id']
    search_fields = ['name', 'price',]
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return Ticket.objects.filter(hospital = hospital_id)   
    
class HospitalTicketsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]
    

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Ticket, hospital = hospital_id, id = id)  
        except Ticket.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

# class HospitalOperationsView(ListCreateAPIView):
#     serializer_class = OperationsSerializer
#     filter_backends = [filters.OrderingFilter, filters.SearchFilter]
#     permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

#     ordering = ['id']
#     search_fields = ['name', 'category__name', "price", "doctor", "code",]
#     def get_queryset(self):
#         hospital_id = self.kwargs['hospital_id']
#         return Operations.objects.filter(hospital = hospital_id)

# class HospitalOperationsDetailView(RetrieveUpdateDestroyAPIView):
#     serializer_class = OperationsSerializer
#     permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

#     def get_object(self):
#         hospital_id = self.kwargs['hospital_id']
#         id = self.kwargs['pk']
#         try:
#             return get_object_or_404(Operations, hospital = hospital_id, id = id)  
#         except Operations.DoesNotExist:
#             return Response(status = status.HTTP_404_NOT_FOUND)
    