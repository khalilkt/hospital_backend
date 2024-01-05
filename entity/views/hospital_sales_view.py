from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from transacations.models.medicament_sale import MedicamentSale, MedicamentSaleSerializer
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from transacations.views.utilis import get_queryset_by_date
from django.db.models import Sum

class HospitalSalesView(ListCreateAPIView):
    serializer_class = MedicamentSaleSerializer

    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    search_fields = ['medicament_sale_items__name', "medicament_sale_items__payed_price", "date", "patient", "insurance_number"]
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        params = self.request.query_params
        year = params.get("year", None)
        month = params.get("month", None)
        day = params.get("day", None)
        ret = MedicamentSale.objects.filter(hospital = hospital_id)
        ret = get_queryset_by_date(ret, year, month, day)
        return ret

    def paginate_queryset(self, queryset):
        params = self.request.query_params 
        all = params.get("all", None)
        if all == "true":
            super().pagination_class.page_size = 1000
        else:
            super().pagination_class.page_size = 10
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        ret =  super().get_paginated_response(data)
        ret.data["total"] = self.get_queryset().aggregate(total = Sum("medicament_sale_items__payed_price"))["total"]
        return ret
class HospitalSalesDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicamentSaleSerializer

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return MedicamentSale.objects.get(hospital=hospital_id, id=id)
        except MedicamentSale.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # override the delete method to delete the related items
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        medicaments = instance.medicament_sale_items.all()
        for medicament in medicaments:
            medicament.medicament.quantity += medicament.quantity
            medicament.medicament.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)