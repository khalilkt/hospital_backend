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
from entity.views import HospitalViewSet, HospitalInventoryView, HospitalInventoryDetailView, HospitalSalesView, HospitalSalesDetailView, HospitalOperationsDetailView, HospitalOperationsView, HospitalAnalysesView, HospitalAnalysesDetailView, HospitalInventoryBulkAddView, HospitalTicketView, HospitalTicketsDetailView
from entity.views import HospitalPaymentsView, HospitalPaymentsDetailView, PaymentViewSet
from transacations.views import HospitalTicketsActionsView, HospitalTicketActionsDetailView, HospitalAnalysesActionsView, HospitalAnalysesActionsDetailView, HospitalOperationActionsView, HospitalOperationActionsDetailView, HospitalSubscribersView
from auth_app.views import LoginTokenView, LoginView , RegisterView
from entity.views.hospital_stats_view import HospitalStatsView, AdminHospitalStatsView, HospitalSalesStatsDetailView, AdminSalesStatsDetailView
from transacations.views.insurances_view import InsuranceViews, TotalInsuranceView
from auth_app.views import UsersViewSet
from entity.views import ClientsView, SubscriptionActionView

router = DefaultRouter()

router.register('hospital', HospitalViewSet, basename='hospital')
router.register('payments', PaymentViewSet, basename='payments')
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('hospital/<int:hospital_id>/clients', ClientsView.as_view(), name='hospital_clients'),
    path('hospital/<int:hospital_id>/clients_subs', SubscriptionActionView.as_view(), name='hospital_clients_subs'),
    path('hospital/<int:hospital_id>/subscribers', HospitalSubscribersView.as_view(), name='hospital_subscribers'),

    path('hospital/<int:hospital_id>/inventory', HospitalInventoryView.as_view(), name='hospital_inventory'),
    path('hospital/<int:hospital_id>/inventory/bulk', HospitalInventoryBulkAddView.as_view(), name='hospital_inventory_bulk_add'),
    path('hospital/<int:hospital_id>/inventory/<int:pk>', HospitalInventoryDetailView.as_view(), name='hospital_inventory_detail'),

    path('hospital/<int:hospital_id>/sales', HospitalSalesView.as_view(), name='hospital_sales'),
    path('hospital/<int:hospital_id>/sales/<int:pk>', HospitalSalesDetailView.as_view(), name='hospital_sales_detail'),

    path('hospital/<int:hospital_id>/operations', HospitalOperationsView.as_view(), name='hospital_operations'),
    path('hospital/<int:hospital_id>/operations/<int:pk>', HospitalOperationsDetailView.as_view(), name='hospital_operations_detail'),

    path('hospital/<int:hospital_id>/tickets', HospitalTicketView.as_view(), name='hospital_tickets'),
    path('hospital/<int:hospital_id>/tickets/<int:pk>', HospitalTicketsDetailView.as_view(), name='hospital_tickets_detail'),

    path('hospital/<int:hospital_id>/payments', HospitalPaymentsView.as_view(), name='hospital_payments'),
    path('hospital/<int:hospital_id>/payments/<int:pk>', HospitalPaymentsDetailView.as_view(), name='hospital_payments_detail'),

    path('hospital/<int:hospital_id>/ticket_actions', HospitalTicketsActionsView.as_view(), name='hospital_tickets_actions'),
    path('hospital/<int:hospital_id>/ticket_actions/<int:pk>', HospitalTicketActionsDetailView.as_view(), name='hospital_tickets_actions_detail'),

    path('hospital/<int:hospital_id>/operation_actions', HospitalOperationActionsView.as_view(), name='hospital_operation_actions'),
    path('hospital/<int:hospital_id>/operation_actions/<int:pk>', HospitalOperationActionsDetailView.as_view(), name='hospital_operation_actions_detail'),

    path('hospital/<int:hospital_id>/analyses_actions', HospitalAnalysesActionsView.as_view(), name='hospital_analyses_actions'),
    path('hospital/<int:hospital_id>/analyses_actions/<int:pk>', HospitalAnalysesActionsDetailView.as_view(), name='hospital_analyses_actions_detail'),
   
    path('hospital/<int:hospital_id>/analyses', HospitalAnalysesView.as_view(), name='hospital_analyses'),
    path('hospital/<int:hospital_id>/analyses/<int:pk>', HospitalAnalysesDetailView.as_view(), name='hospital_analyses_detail'),


    path('hospital/<int:hospital_id>/stats', HospitalStatsView.as_view(), name='hospital_stats'),
    path('hospital/<int:hospital_id>/stats/sales', HospitalSalesStatsDetailView.as_view(), name='hospital_sales_stats'),
    path('stats/', AdminHospitalStatsView.as_view(), name='admin_stats'),
    path('stats/sales', AdminSalesStatsDetailView.as_view(), name='admin_sales_stats'),

    path('login/', LoginView.as_view(), name='login'), 
    path('login_token/', LoginTokenView.as_view(), name='login_token'),
    path('register/', RegisterView.as_view(), name='register'),

    path("hospital/<int:hospital_id>/insurances", InsuranceViews.as_view(), name="hospital_insurances"),
    path("hospital/<int:hospital_id>/insurances/total", TotalInsuranceView.as_view(), name="hospital_insurances_total"),


]


urlpatterns += router.urls


