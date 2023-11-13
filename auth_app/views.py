from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from entity.models import Hospital, HospitalSerializer
# Create your views here.

class LoginTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if token is None:
            return Response({"error" : "Token is required"}, status=400)
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({"error" : "Invalid token"}, status=400)
        user : User = token.user
        hospitals = []
        if not  user.is_superuser :

            if Hospital.objects.filter(assignedUser = user).exists():
                hospitals = [HospitalSerializer(Hospital.objects.get(assignedUser = user)).data]
        else:
            hospitals = HospitalSerializer(Hospital.objects.all(), many=True).data

        return Response({
            'token': token.key,
            'user_id': user.pk,
            "is_admin" : user.is_superuser, 
            "hospitals" : hospitals
        })

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        hospitals = []
        if not  user.is_superuser :

            if Hospital.objects.filter(assignedUser = user).exists():
                hospitals = [HospitalSerializer(Hospital.objects.get(assignedUser = user)).data]
        else:
            hospitals = HospitalSerializer(Hospital.objects.all(), many=True).data
    
        return Response({
            'token': token.key,
            'user_id': user.pk,
            "is_admin" : user.is_superuser, 
            "hospitals" : hospitals
        })
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_staff', 'is_superuser', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny  )