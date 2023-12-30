from django.db import models
from rest_framework import serializers

class Medicament(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    hospital = models.ForeignKey('entity.Hospital', on_delete=models.CASCADE, related_name='medicament')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicamentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context and "request" in self.context and  self.context['request'].method == 'POST' and "hospital_id" in self.context:
            self.initial_data["hospital"] = self.context["hospital_id"]
    
    class Meta:
        model = Medicament
        fields = "__all__"  