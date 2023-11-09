from http.client import METHOD_NOT_ALLOWED
from rest_framework import viewsets
from entity.models import Hospital, HospitalSerializer

class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        # get user from request
        user = self.request.user
        return Hospital.objects.all() 

    def destroy(self, request, *args, **kwargs):
        raise METHOD_NOT_ALLOWED('DELETE')