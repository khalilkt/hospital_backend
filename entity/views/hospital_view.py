from http.client import METHOD_NOT_ALLOWED
from rest_framework import viewsets
from entity.models import Hospital, HospitalSerializer
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated, NOT, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from entity.models.hospital import HopsitalPermission

class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'staff_members__name']
    ordering = ['id']
    queryset  = Hospital.objects.all()
    permission_classes = [IsAuthenticated,HopsitalPermission]
    
    # def get_permissions(self):
    #     print("get_permissions")
    #     print(self.request.user.is_staff())
    #     if self.action == 'list':
    #         print("list")
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes =  [IsAuthenticated, IsHospitalAssignedUser]
    #     return [permission for permission in permission_classes]  
            
        
    # def destroy(self, request, *args, **kwargs):
    #     raise METHOD_NOT_ALLOWED('DELETE')