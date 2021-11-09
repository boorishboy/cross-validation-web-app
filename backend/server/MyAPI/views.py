from django.shortcuts import render
from django.views.generic import View, DetailView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from . serializers import ParametersSerializer, resultsOLSSerializer, ResultsNNLSSerializer
from . models import Parameters, ResultsNNLS, ResultsOLS
from . forms import ParametersForm
import pandas as pd
from django.conf import settings
from . import MLModel
from collections import namedtuple
from django.shortcuts import redirect, get_object_or_404
import ast
from django.http import HttpResponseRedirect
from django.urls import reverse
import time
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dashboard.html', {})

class ParametersView(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer

class ResultDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'results/result_detail.html', {})

class ResultsOLSView(viewsets.ModelViewSet):
    queryset = ResultsOLS.objects.all()
    serializer_class = resultsOLSSerializer

class ResultsNNLSView(viewsets.ModelViewSet):
    queryset = ResultsNNLS.objects.all()
    serializer_class = ResultsNNLSSerializer




def stringToList(string):
    list = string.split(', ')
    return str(list)


def stringToDict(string):
    inputString = "{" + string + "}"
    return inputString


def myform(request):
    if request.method == 'POST':
        form = ParametersForm(request.POST, request.FILES)
        if form.is_valid():
            inputFile = request.FILES['inputFile'].read()
            paramList = stringToList(form.cleaned_data['paramList'])
            targetColumn = form.cleaned_data['targetColumn']
            adjust = form.cleaned_data['adjust']
            round = form.cleaned_data['round']
            if form.cleaned_data['fixed'] is not None:
                fixed = stringToDict(form.cleaned_data['fixed'])
            else:
                fixed = form.cleaned_data['fixed']
            threshold = form.cleaned_data['threshold']
            path = settings.TMP_FILES + '/data.csv'
            with open(path, 'w+b') as f:
                f.write(inputFile)
                f.close()
            data = pd.read_csv(path)
            form.save()
            resultOLS, resultNNLS = MLModel.get_data(data, paramList, targetColumn,
                              adjust, round, threshold)
            resultOLS.runid = Parameters.objects.latest('runid')
            resultNNLS.runid = Parameters.objects.latest('runid')
            resultOLS.save()
            resultNNLS.save()




    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})

# def result_detail(request, pk):
#         result_detail_ols = get_object_or_404(ResultsOLS, pk=pk)
#         result_detail_nnls = get_object_or_404(ResultsNNLS, pk=pk)
#         content = {
#             'result_detail_ols': result_detail_ols,
#             'result_detail_nnls': result_detail_nnls,
#         }
#         return render(request, 'results/result_detail.html', context)
