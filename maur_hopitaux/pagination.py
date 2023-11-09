from rest_framework import pagination
from rest_framework.response import Response

class MPagePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page' : self.page.number,
            'total_pages': self.page.paginator.num_pages,        
            'data': data,  
        })
