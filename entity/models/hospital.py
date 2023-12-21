from django.db import models
from rest_framework import serializers
from auth_app.models import UserSerializer
from entity.models.hospital_tickets import TicketSerializer
from entity.models.medicament import MedicamentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from transacations.models.payment import Payment, PaymentSerializer

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    has_pharmacy = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False) # if yes then we will only have tickets
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class HospitalSerializer(serializers.ModelSerializer):
    # staff = serializers.SlugRelatedField(many=True, read_only=True, slug_field='staff_members')
    tickets = TicketSerializer(many=True, read_only=True)
    payments = serializers.SerializerMethodField()

    def get_payments(self, obj):
        ret = Payment.objects.filter(hospital=obj).order_by('-created_at')[:3]
        return PaymentSerializer(ret, many=True).data
    
    class Meta:
        model = Hospital
        fields = "__all__"

class HopsitalPermission(BasePermission):
    def has_permission(self, request, view):

        user : User = request.user
        if not user :
            return False
        if view.action == 'list' or view.action == 'destroy' :
            return user.is_staff()
        return True
    
    def has_object_permission(self, request, view, obj):

        user : User = request.user 
        if not user :
            return False 
        return user.assigned_hospital == obj or user.is_staff()
    
    
class IsHospitalDetailsAssignedUser(BasePermission):   
    def has_permission(self, request, view):
        user : User = request.user
        if user.is_staff() :
            return True
        
        if not user.assigned_hospital :
            return False
        
        hospital_id = view.kwargs['hospital_id']
        if not hospital_id :
            return False
        return user.assigned_hospital.id == hospital_id
        