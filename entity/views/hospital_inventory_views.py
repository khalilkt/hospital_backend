from rest_framework.views import APIView
from entity.models import Hospital, Medicament, MedicamentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from entity.models.hospital import IsHospitalDetailsAssignedUser
from transacations.models  import OperationAction, AnalyseAction, MedicamentSale, TicketAction, MedicamentSaleItem, Payment

class HospitalInventoryView(ListCreateAPIView):
    serializer_class = MedicamentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated, IsHospitalDetailsAssignedUser]
    ordering = ['id']
    search_fields = ['name', "price"]

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
        


class HospitalInventoryAlertView(APIView):
    def get(self, request, hospital_id):
        ret = Medicament.objects.filter(hospital = hospital_id, quantity__lte = 10).order_by("quantity")
        serializer = MedicamentSerializer(ret, many=True, context={"request" : request})
        return Response(serializer.data)

class HospitalInventoryBulkAddView(APIView):
    def post(self, request, hospital_id):
        data = request.data
        if not isinstance(data, list):
            return Response({"error" : "data should be a list"}, status=400)

        for item in data:
            item["hospital"] = hospital_id
            if not "name" in item:
                return Response({"error" : "name is required"}, status=400)
            if Medicament.objects.filter(hospital = hospital_id, name = item["name"]).exists():
                medic = Medicament.objects.get(hospital = hospital_id, name = item["name"]) 
                item["quantity"] = item["quantity"] + medic.quantity
                medic = MedicamentSerializer(medic, data=item)
                if medic.is_valid():
                    medic.save()
                else:
                    return Response(medic.errors, status = 400)
            else:
                serializer = MedicamentSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status = 400)
        return Response(status = 200)
    
class HospitalInventoryAllView(APIView):
    def get(self, request, hospital_id):
        # return clear_actions()
        ret = Medicament.objects.filter(hospital = hospital_id).order_by("quantity")
        serializer = MedicamentSerializer(ret, many=True, context={"request" : request})
        return Response(serializer.data)
    
def clear_actions():
    OperationAction.objects.all().delete()
    AnalyseAction.objects.all().delete()
    MedicamentSale.objects.all().delete()
    MedicamentSaleItem.objects.all().delete()
    TicketAction.objects.all().delete()
    Payment.objects.all().delete()

    return Response(status = 200)