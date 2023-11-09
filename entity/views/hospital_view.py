from http.client import METHOD_NOT_ALLOWED
from rest_framework import viewsets
from entity.models import Hospital, HospitalSerializer
from rest_framework import filters

class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'adresse']
    queryset  = Hospital.objects.all()



    def destroy(self, request, *args, **kwargs):
        raise METHOD_NOT_ALLOWED('DELETE')