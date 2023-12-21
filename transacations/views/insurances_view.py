from rest_framework.generics import  ListAPIView, RetrieveAPIView
from transacations.models import OperationAction, AnalyseAction , MedicamentSale, TicketAction
from entity.models import Hospital
from django.db.models import F, CharField, Sum , DecimalField
from rest_framework import serializers
from django.db.models import Value
from django.db.models.functions import Concat


class InssuranceSerializer(serializers.Serializer):
    name = serializers.CharField()
    insurance_number = serializers.CharField()
    price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    iid  = serializers.CharField() 

class InsuranceViews(ListAPIView):
    serializer_class = InssuranceSerializer
    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        ret = OperationAction.objects.filter(insurance_number__isnull=False, operation__hospital= hospital_id).annotate(name = F('operation__name'), iid = Concat(Value("op_"), F("id"), output_field=CharField())).union(
            AnalyseAction.objects.filter(insurance_number__isnull=False,analyse__hospital= hospital_id).annotate(name = F('analyse__name'), iid = Concat(Value("an_"), F("id"), output_field=CharField()))
        ).union(
            MedicamentSale.objects.filter(insurance_number__isnull=False, hospital= hospital_id).annotate( price = Sum(F("medicament_sale_items__sale_price") * F("medicament_sale_items__quantity")) , name = Value("Vente de medicament", output_field=CharField()), iid = Concat(Value("sl_"), F("id"), output_field=CharField()))
        ).union(
            TicketAction.objects.filter(insurance_number__isnull=False, ticket__hospital= hospital_id).annotate(name = Value('Ticket Sale', output_field=CharField()), iid = Concat(Value("tk_"), F("id"), output_field=CharField()))
        ).values( 'name', 'created_at', 'insurance_number', 'price',"iid",).order_by('-created_at')
        return ret 
