from rest_framework import serializers
from . models import Parameters, Results


class ResultsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Results
		fields = '__all__'


class ParametersSerializer(serializers.ModelSerializer):
	results = ResultsSerializer(read_only=True)
	class Meta:
		model=Parameters
		# fields = '__all__'
		fields=['runid', 'upload_timestamp', 'file_hash', 'inputFile', 'paramList', 'targetColumn', 'adjust', 'round', 'fixed', 'threshold', 'results']
