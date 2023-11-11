from django.db import models
from rest_framework import serializers
from entity.models.medicament import MedicamentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    # foreign key to the django user model
    assignedUser = models.OneToOneField(User, related_name='hospital', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"

class IsHospitalAssignedUser(BasePermission):   
    def has_object_permission(self, request, view, obj  ):
        user : User  = request.user
        print("------------------")
        if not user :
            print("user is none")
            return False  
        print("has_object_permission")
        print(user.username)    
        if (obj.assignedUser):
            print(obj.assignedUser.username)
        else :
            print("None")
        print("------------------")
        return user.is_superuser or obj.assignedUser == user
    
class IsHospitalDetailsAssignedUser(BasePermission):   

    def has_permission(self, request, view):
        user : User = request.user
        if user.is_superuser :
            return True
        if not user.hospital :
            return False
        hospital_id = view.kwargs['hospital_id']
        if not hospital_id :
            return False
        return user.hospital.id == hospital_id
        