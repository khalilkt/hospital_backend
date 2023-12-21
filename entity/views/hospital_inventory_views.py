from rest_framework.views import APIView
from entity.models import Hospital, Medicament, MedicamentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser

class HospitalInventoryView(ListCreateAPIView):
    serializer_class = MedicamentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser]
    ordering = ['id']
    search_fields = ['name', "codebarres", "price"]

    def get_serializer_context(self):
        hospital_id = self.kwargs['hospital_id']    
        context =  super().get_serializer_context()
        context['hospital_id'] = hospital_id
        return context

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        if not Hospital.objects.filter(id = hospital_id).exists():
            return Response({"error" : "Hospital not found"}, status = status.HTTP_404_NOT_FOUND)
        return Medicament.objects.filter(hospital = hospital_id)

class HospitalInventoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicamentSerializer
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser ]
    

    def get_object(self):
        hospital_id = self.kwargs['hospital_id']
        id = self.kwargs['pk']
        try:
            return get_object_or_404(Medicament, hospital = hospital_id, id = id)  
        except Medicament.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
# create a bulk add view

class HospitalInventoryBulkAddView(APIView):
    def post(self, request, hospital_id):
        data = request.data
        if not isinstance(data, list):
            return Response({"error" : "data should be a list"}, status=400)
        # for item in data:
        #     if not "name" in item:
        #         return Response({"error" : "name is required"}, status=400)
        #     if not "category" in item:
        #         return Response({"error" : "category is required"}, status=400)
        #     if not "codebarres" in item:
        #         return Response({"error" : "codebarres is required"}, status=400)
        #     if not "price" in item:
        #         return Response({"error" : "price is required"}, status=400)
        #     if not "quantity" in item:
        #         return Response({"error" : "quantity is required"}, status=400)
        #     if not "description" in item:
        #         return Response({"error" : "description is required"}, status=400)
        for item in data:
            item["hospital"] = hospital_id
        serializer = MedicamentSerializer(data=data, many=True, context={"request" : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status = 400)