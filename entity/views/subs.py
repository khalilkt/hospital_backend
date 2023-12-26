from rest_framework import viewsets
from  entity.models.subs import Client, ClientSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F, Value, CharField, IntegerField, Q, Sum, Count, When , Case, BooleanField, ExpressionWrapper, DateField, DateTimeField, DurationField

class ClientsView(ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, )

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'hospital__name']
    

    def get_queryset(self):
        is_active = self.request.query_params.get('is_active', None) 
        hospital_id = self.kwargs['hospital_id']    
        ret = Client.objects.with_status().filter(hospital = hospital_id)
        if is_active == "active":
            ret = ret.filter(is_active = True)
        elif is_active == "inactive":
            ret = ret.filter(is_active = False)
                
        return ret
    
class SubscriptionActionView(ListCreateAPIView):
    # serializer_class = SubscriptionActionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    # def get_queryset(self):
    #     hospital_id = self.kwargs['hospital_id']    
    #     return SubscriptionAction.objects.filter(client__hospital = hospital_id)
    