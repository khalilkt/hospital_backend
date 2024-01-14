from django.db import models
from rest_framework import serializers
from auth_app.models import UserSerializer
from entity.models.hospital_tickets import TicketSerializer
from entity.models.medicament import MedicamentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from .municipal_tax import MunicipalTaxDataSerializer


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    has_pharmacy = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False) # if yes then we will only have tickets
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    subscription_price = models.IntegerField(null = True, blank = True)
    show_in_subs = models.BooleanField(default=False)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    bank_account = models.CharField(max_length=255) 
    ticket_name  = models.CharField(max_length=255, null=True, blank=True)

class StaffSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class HospitalSerializer(serializers.ModelSerializer):
    # staff = serializers.SlugRelatedField(many=True, read_only=True, slug_field='staff_members')
    tickets = TicketSerializer(many=True, read_only=True)
    staff = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='staff_members')
    has_subscription = serializers.SerializerMethodField()
    stock_alerts = serializers.SerializerMethodField()
    staff_data = StaffSerializer(many=True, read_only=True, source='staff_members')
    municipal_tax_data = MunicipalTaxDataSerializer(read_only=True)
    is_municipal = serializers.BooleanField(write_only=True)
    
    def get_stock_alerts(self, obj):
        ret = obj.medicament.filter(quantity__lte = 10)
        return MedicamentSerializer(ret, many=True).data
    

    def get_has_subscription(self, obj):
        return obj.tickets.filter(is_subscription=True).exists()

    class Meta:
        model = Hospital
        fields = "__all__"

    def create(self, validated_data):
        is_municipal = validated_data.pop("is_municipal", False)
        ret = super().create(validated_data)
        if is_municipal:
            from entity.models.municipal_tax import MunicipalTaxData
            MunicipalTaxData.objects.create(hospital=ret)
        return ret


    

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
        return user.assigned_hospital == obj or user.is_staff() or user.is_superuser
    
    
class IsHospitalDetailsAssignedUser(BasePermission):   
    def has_permission(self, request, view):
        user : User = request.user
        if user.is_staff() or user.is_superuser :
            return True
        
        if not user.assigned_hospital :
            return False
        
        hospital_id = view.kwargs['hospital_id']
        if not hospital_id :
            return False
        return user.assigned_hospital.id == hospital_id
        