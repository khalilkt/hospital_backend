from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from entity.models.analyse_categories import AnalyseCategorySerializer, AnalyseCategory
from rest_framework.response import Response
from rest_framework import status

class CreateAnalyseCategoryView(APIView):
    def post(self, request, hospital_id):
        serializer = AnalyseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hospital_id=hospital_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

class AnalyseCategoriesView(ListCreateAPIView):
    serializer_class = AnalyseCategorySerializer
    pagination_class = None

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return AnalyseCategory.objects.filter(hospital=hospital_id)
    
        
