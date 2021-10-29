from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from . serializers import parametersSerializer, resultSerializer, resultsOLSSerializer, resultsNNLSSerializer
from . models import Parameters, ResultsNNLS, ResultsOLS
from . forms import ParametersForm
import pandas as pd
from django.conf import settings
from . import MLModel
from collections import namedtuple
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dashboard.html', {})

class ParametersView(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = parametersSerializer

# ResultResponse = namedtuple('ResultResponse', ('resultsNNLS', 'resultsOLS'))


# class ResultsView(viewsets.ViewSet):
#     def list(self, request):
#         resultResponse = ResultResponse(
#             resultsNNLS=ResultsNNLS.objects.all(),
#             resultsOLS=ResultsOLS.objects.all(),
#         )
#         serializer = resultSerializer(resultResponse)
#         return Response(serializer.data)
#
#     def destroy(self, request):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ResultsOLSView(viewsets.ModelViewSet):
    queryset = ResultsOLS.objects.all()
    serializer_class = resultsOLSSerializer

class ResultsNNLSView(viewsets.ModelViewSet):
    queryset = ResultsNNLS.objects.all()
    serializer_class = resultsNNLSSerializer



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
            MLModel.get_data(data, paramList, targetColumn,
                              adjust, round, threshold)
        return redirect('/dashboard/')

    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})
