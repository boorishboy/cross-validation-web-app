from rest_framework import serializers
from . models import Parameters

class parametersSerializer(serializers.ModelSerializer):
	class Meta:
		model=Parameters
		fields='__all__'
