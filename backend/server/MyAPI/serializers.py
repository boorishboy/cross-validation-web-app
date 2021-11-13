from rest_framework import serializers
from . models import Parameters, ResultsNNLS, ResultsOLS


class resultsOLSSerializer(serializers.ModelSerializer):
	class Meta:
		model=ResultsOLS
		fields = '__all__'

class ResultsNNLSSerializer(serializers.ModelSerializer):
	class Meta:
		model=ResultsNNLS
		fields = '__all__'

class ParametersSerializer(serializers.ModelSerializer):
	resultsols = resultsOLSSerializer(read_only=True, many=True)
	resultsnnls = ResultsNNLSSerializer(read_only=True, many=True)
	class Meta:
		model=Parameters
		# fields = '__all__'
		fields=['runid', 'inputFile', 'paramList', 'targetColumn', 'adjust', 'round', 'fixed', 'threshold', 'resultsnnls', 'resultsols']
	# def create(self, validated_data):
	# 	resultsnnls_data = validated_data.pop('resultsNNLS')
	# 	resultsols_data = validated_data.pop('resultsOLS')
	# 	parameters = Parameters.objects.create(**validated_data)
	# 	for resultnnls in resultsnnls_data:
	# 		ResultsNNLS.objects.create(parameters=parameters, **resultnnls)
	# 	for resultols in resultsols_data:
	# 		ResultsOLS.objects.create(parameters=parameters, **resultols)
	# 	return parameters
