from rest_framework.views import APIView
from transacations.models import TicketAction, TicketActionSerializer
from entity.models import Hospital
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from rest_framework import viewsets

class HospitalTicketsActionsView(ListCreateAPIView):
    serializer_class = TicketActionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    ordering = ['id']
    search_fields = ["ticket__name"]
    
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return TicketAction.objects.filter(ticket__hospital = hospital_id)   

class HospitalTicketActionsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketActionSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser, ]

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(TicketAction, ticket__hospital = hospital_id, id = id)  
        except TicketAction.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
