"""maur_hopitaux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from entity.views import HospitalViewSet, HospitalInventoryView, HospitalInventoryDetailView, HospitalSalesView, HospitalSalesDetailView, MedicamentCategoriesView, OperationCategoriesView, HospitalOperationsDetailView, HospitalOperationsView


router = DefaultRouter()

router.register('hospital', HospitalViewSet, basename='hospital')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hospital/<int:hospital_id>/inventory', HospitalInventoryView.as_view(), name='hospital_inventory'),
    path('hospital/<int:hospital_id>/inventory/<int:pk>', HospitalInventoryDetailView.as_view(), name='hospital_inventory_detail'),

    path('hospital/<int:hospital_id>/sales', HospitalSalesView.as_view(), name='hospital_sales'),
    path('hospital/<int:hospital_id>/sales/<int:pk>', HospitalSalesDetailView.as_view(), name='hospital_sales_detail'),

    path('hospital/<int:hospital_id>/medicament_categories', MedicamentCategoriesView.as_view(), name='medicament_categories'),
    path('hospital/<int:hospital_id>/operation_categories', OperationCategoriesView.as_view(), name='operation_categories'),

    path('hospital/<int:hospital_id>/operations', HospitalOperationsView.as_view(), name='hospital_operations'),
    path('hospital/<int:hospital_id>/operations/<int:pk>', HospitalOperationsDetailView.as_view(), name='hospital_operations_detail'),
]


urlpatterns += router.urls


