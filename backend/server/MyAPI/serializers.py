from rest_framework import serializers
from . models import Parameters, ResultsNNLS, ResultsOLS

class parametersSerializer(serializers.ModelSerializer):
	class Meta:
		model=Parameters
		fields='__all__'

class resultsOLSSerializer(serializers.ModelSerializer):
	class Meta:
		model=ResultsOLS
		fields='__all__'

class resultsNNLSSerializer(serializers.ModelSerializer):
	class Meta:
		model=ResultsNNLS
		fields='__all__'

class resultSerializer(serializers.Serializer):
	resultsNNLS = resultsNNLSSerializer(many=True)
	resultsOLS = resultsOLSSerializer(many=True)
