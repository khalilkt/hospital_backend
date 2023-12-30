from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from transacations.models.medicament_sale import MedicamentSale, MedicamentSaleSerializer
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

class HospitalSalesView(ListCreateAPIView):
    serializer_class = MedicamentSaleSerializer

    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    search_fields = ['medicament__name', "date", "price"]
    def get_queryset(self):
        return MedicamentSale.objects.filter(hospital=self.kwargs['hospital_id'])


class HospitalSalesDetailView(RetrieveUpdateAPIView):
    serializer_class = MedicamentSaleSerializer

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return MedicamentSale.objects.get(hospital=hospital_id, id=id)
        except MedicamentSale.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
