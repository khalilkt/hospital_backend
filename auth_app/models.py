from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers

class UserManager(BaseUserManager):
    def create_user(self, username, name,is_superuser,  password):
        if not username or len(username.strip()) < 3:
            raise ValueError('Users must have an username with at least 3 characters')
        if not password:
            raise ValueError('Users must have a password')
        if not name or name == "": 
            raise ValueError('Users must have a name')
        user = self.model( username=username, name = name, is_superuser = is_superuser or False)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username,name,is_superuser,  password):
        user = self.create_user(username=username, name = name,  password=password)
        user.is_admin = True
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser): 
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    USERNAME_FIELD = 'username'
    assigned_hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='staff_members', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    objects = UserManager()
    REQUIRED_FIELDS = ['name']

    def is_staff(self):
        return self.is_admin

class UserSerializer(serializers.ModelSerializer):
    assigned_hospital_name = serializers.CharField(source='assigned_hospital.name', read_only=True)
    
    def create(self, validated_data):
        if "is_admin" in validated_data and  validated_data['is_admin']:
            user = User.objects.create_superuser(username=validated_data['username'],is_superuser = validated_data.get("is_superuser", False), password=validated_data['password'], name=validated_data['name'])
            return user
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'], name=validated_data['name'], is_superuser = validated_data.get("is_superuser", False))
        user.assigned_hospital = validated_data['assigned_hospital']
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.assigned_hospital = validated_data.get('assigned_hospital', instance.assigned_hospital)
        instance.username = validated_data.get('username', instance.username)   
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = "__all__" 
        extra_kwargs = {'assigned_hospital': {'required': True}, 'password': {'write_only': True}} 




