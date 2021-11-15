from django.shortcuts import render
from django.views.generic import View, DetailView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from . serializers import ParametersSerializer, ResultsSerializer
from . models import Parameters, Results
from . forms import ParametersForm
import pandas as pd
from django.conf import settings
from . import MLModel
from collections import namedtuple
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
import os
import hashlib
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

class ResultsView(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer

# class ResultsOLSView(viewsets.ModelViewSet):
#     queryset = ResultsOLS.objects.all()
#     serializer_class = resultsOLSSerializer
#
# class ResultsNNLSView(viewsets.ModelViewSet):
#     queryset = ResultsNNLS.objects.all()
#     serializer_class = ResultsNNLSSerializer


def stringToList(string):
    list = string.split(', ')
    return str(list)


def stringToDict(string):
    inputString = "{" + string + "}"
    return inputString

def get_checksum(file):
    hash = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash.update(chunk)
    return hash.hexdigest()


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
            # Use process PID to distinguish data files between instances
            path = settings.TMP_FILES + '/data' + str(os.getpid()) + '.csv'
            parameters = form.save(commit=False)
            with open(path, 'w+b') as f:
                f.write(inputFile)
                f.close()
            data = pd.read_csv(path)
            upload_timestamp = datetime.now()
            parameters.upload_timestamp = upload_timestamp
            file_hash = get_checksum(request.FILES['inputFile'])
            parameters.file_hash = file_hash
            parameters.save()
            results = MLModel.get_data(data, paramList, targetColumn,
                              adjust, round, threshold)
            results.file_hash = file_hash
            results.upload_timestamp = upload_timestamp
            results.runid = Parameters.objects.latest('runid')
            results.save()
            os.remove(path)



    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})
