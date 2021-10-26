from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from . serializers import parametersSerializer
from . models import Parameters
from . forms import ParametersForm
import pandas as pd
import csv
from django.conf import settings
from . import MLModel
# Create your views here.

class ParametersView(viewsets.ModelViewSet):
	queryset = Parameters.objects.all()
	serializer_class = parametersSerializer


def myform(request):
    if request.method == 'POST':
        form = ParametersForm(request.POST, request.FILES)
        if form.is_valid():
            inputFile = request.FILES['inputFile'].read()
            paramList = form.cleaned_data['paramList']
            targetColumn = form.cleaned_data['targetColumn']
            adjust = form.cleaned_data['adjust']
            round = form.cleaned_data['round']
            fixed = form.cleaned_data['fixed']
            threshold = form.cleaned_data['threshold']
            path = settings.TMP_FILES + '/data.csv'
            with open(path, 'w+b') as f:
                f.write(inputFile)
                f.close()
            data = pd.read_csv(path)

    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})


# def DataProcessing(data, paramList, targetColumn, adjust, round, fixed, threshold):

#     NNLS = 0
#     OLS = 1
#
#     y = df.loc[:,target_column].values
#     # Adjust the regressand.
#     y = y * adjust
#     fixed = "{}"
#     param_value_dict = eval(fixed)
#     fixed_params = param_value_dict.keys()
#     unconstrained_params = []
