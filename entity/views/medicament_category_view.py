from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from entity.models.medicament_category import MedicamentCategorySerializer, MedicamentCategory
from rest_framework.response import Response
from rest_framework import status

class CreateMedicamentCategoryView(APIView):
    def post(self, request, hospital_id):
        serializer = MedicamentCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hospital_id=hospital_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

class MedicamentCategoriesView(ListCreateAPIView):
    serializer_class = MedicamentCategorySerializer
    pagination_class = None

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return MedicamentCategory.objects.filter(hospital=hospital_id)
    
        
