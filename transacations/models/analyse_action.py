
from django.db import models
from django.conf import settings
from rest_framework import serializers

class AnalyseAction(models.Model) :
    analyse = models.ForeignKey('entity.Analyses', on_delete=models.CASCADE, related_name='actions')
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    patient     = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='analyse_actions', on_delete=models.SET_NULL, null=True, blank=True)

class AnalyseActionSerializer(serializers.ModelSerializer):
    about = serializers.CharField(source='analyse.about', read_only=True)
    analyse_name = serializers.CharField(source='analyse.name', read_only=True)
    def __init__(self, instance=None, data=None,context = None, **kwargs):
        if context and "request" in context and  context["request"].method == "POST": 
            current_user = context['request'].user
            data['created_by'] = current_user.id
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = AnalyseAction
        fields = "__all__"
        extra_kwargs = {
            'created_by': {'required': True},
        }