from django.shortcuts import render
from django.views.generic import View, DetailView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from . serializers import InputSerializer, ResultsSerializer, CombinedSerializer
from . models import Parameters, Results
from . forms import ParametersForm
import pandas as pd
from django.conf import settings
from . import MLModel
from collections import namedtuple
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import os
import hashlib
import json
# Create your views here.


def columnsToCheckboxes(file):
    col_list = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()
    col_response = json.dumps(col_list)


def stringToList(string):
    list = string.split(', ')
    return str(list)


def stringToDict(string):
    inputString = "{" + string + "}"
    return inputString



def input(request):
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
            hash = hashlib.md5()
            # with open(path, 'w+b') as f:
            #     for chunk in iter(lambda: f.read(4096), b""):
            #         hash.update(chunk)
            #     parameters.file_hash = hash.hexdigest()
            #     f.write(inputFile)
            #     f.close()
            with open(path, 'wb+') as f:
                f.write(inputFile)
                f.seek(0)
                hash.update(f.read())
                file_hash = hash.hexdigest()
                f.close()
            data = pd.read_csv(path)
            upload_timestamp = timezone.now()
            parameters.upload_timestamp = upload_timestamp
            # file_hash = get_checksum(request.FILES['inputFile'].read())
            parameters.file_hash = file_hash

            results = MLModel.get_data(data, paramList, targetColumn,
                              adjust, round, fixed, threshold)
            parameters.save()
            results.file_hash = file_hash
            results.upload_timestamp = upload_timestamp
            results.runid = Parameters.objects.latest('runid')
            results.pk = None
            results.save()
            os.remove(path)
            return redirect('/dashboard/')


    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        parameters = Parameters.objects.all()
        return render(request, 'dashboard/dashboard.html', {'parameters': parameters})

class CombinedView(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = CombinedSerializer

class InputView(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = InputSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create()


    def perform_create(self, serializer):
        upload_timestamp = timezone.now()
        inputFile = self.request.FILES['inputFile'].read()
        paramList = stringToList(serializer.validated_data['paramList'])
        targetColumn = serializer.validated_data['targetColumn']
        try:
            adjust = serializer.validated_data['adjust']
        except KeyError:
            adjust = None
        round = serializer.validated_data['round']
        try:
            fixed = stringToDict(serializer.validated_data['fixed'])
        except KeyError:
            fixed = None
        threshold = serializer.validated_data['threshold']
        path = settings.TMP_FILES + '/data' + str(os.getpid()) + '.csv'
        hash = hashlib.md5()
        with open(path, 'wb+') as f:
            f.write(inputFile)
            f.seek(0)
            hash.update(f.read())
            file_hash = hash.hexdigest()
            f.close()
        data = pd.read_csv(path)
        results = MLModel.get_data(data, paramList, targetColumn,
                          adjust, round, fixed, threshold)
        results.file_hash = file_hash
        serializer.save(file_hash=file_hash)
        results.pk = None
        print(results.pk)
        results.runid = Parameters.objects.latest('runid')
        results.upload_timestamp = upload_timestamp
        os.remove(path)
        results.save()


class ResultsView(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer

class ResultDetailView(View):
    def get(self, request, *args, **kwargs):
        parameters = get_object_or_404(Parameters, runid=kwargs['pk'])
        results = get_object_or_404(Results, runid=kwargs['pk'])
        return render(request, 'results/result_detail.html', {'parameters': parameters, 'results': results})
