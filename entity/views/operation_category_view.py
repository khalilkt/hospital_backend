from rest_framework.generics import ListCreateAPIView , ListAPIView
from rest_framework.views import APIView
from entity.models.operation_category import OperationCategory, OperationCategorySerializer
from rest_framework.response import Response
from rest_framework import status

class OperationCategoriesView(ListAPIView):
    serializer_class = OperationCategorySerializer
    pagination_class = None

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return OperationCategory.objects.filter(hospital=hospital_id)