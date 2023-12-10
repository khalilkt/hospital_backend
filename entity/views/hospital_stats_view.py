# view for hospital stats

import datetime
from rest_framework.views import APIView
from entity.models import Hospital
from rest_framework.response import Response
from entity.models.analyses import Analyses
from entity.models.medicament import Medicament

from entity.models.operation import Operations
from transacations.models.medicament_sale import MedicamentSale

class HospitalStatsView(APIView):
    def get(self, request, hospital_id):
        current_date  = datetime.datetime.now().date()

        ret  = Hospital.objects.get(id=hospital_id)
        operations_len = ret.operations.all().count()
        analyses_len = ret.analyses.all().count()
        medicaments_len = ret.medicament.all().count()
        total_sales_len = ret.medicamentsale_set.all().count()
        month_sales_len = ret.medicamentsale_set.filter(created_at__month = current_date.month).filter(created_at__year = current_date.year).count()
        today_sales_len = ret.medicamentsale_set.filter(created_at = current_date).count()

        week_sales = {

        }
        # current date should be equal to the first monday of the week
        current_date = current_date - datetime.timedelta(days=current_date.weekday())
        for i in range(7):
            week_sales[ str(current_date.weekday())] = ret.medicamentsale_set.filter(created_at = current_date).count()
            current_date = current_date + datetime.timedelta(days=1)
    
        return Response({
            "operations": operations_len,
            "analyses": analyses_len,
            "medicaments": medicaments_len,
            "total_sales": total_sales_len,
            "month_sales": month_sales_len,
            "today_sales": today_sales_len,
            "week_sales": week_sales
        })
    

class AdminHospitalStatsView(APIView):
     def get(self, request):
        current_date  = datetime.datetime.now().date()
        operations_len = Operations.objects.all().count()
        analyses_len = Analyses.objects.all().count()
        medicaments_len = Medicament.objects.all().count()

        total_sales_len = MedicamentSale.objects.all().count()
        
        month_sales_len = MedicamentSale.objects.filter(created_at__month = current_date.month).filter(created_at__year = current_date.year).count()
        today_sales_len = MedicamentSale.objects.filter(created_at = current_date).count()

        week_sales = {}
        # current date should be equal to the first monday of the week
        current_date = current_date - datetime.timedelta(days=current_date.weekday())
        for i in range(7):
            week_sales[ str(current_date.weekday())] = MedicamentSale.objects.filter(created_at = current_date).count()
            current_date = current_date + datetime.timedelta(days=1)
    
        return Response({
            "operations": operations_len,
            "analyses": analyses_len,
            "medicaments": medicaments_len,
            "total_sales": total_sales_len,
            "month_sales": month_sales_len,
            "today_sales": today_sales_len,
            "week_sales": week_sales
        })