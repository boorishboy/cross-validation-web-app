from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from . serializers import parametersSerializer
from . models import Parameters
from . forms import ParametersForm
# Create your views here.

class ParametersView(viewsets.ModelViewSet):
	queryset = Parameters.objects.all()
	serializer_class = parametersSerializer

def myform(request):
    if request.method == 'POST':
        form = ParametersForm(request.POST)
        if form.is_valid():
            inputFile = form.cleaned_data['inputFile']
            paramList = form.cleaned_data['paramList']
            targetColumn = form.cleaned_data['targetColumn']
            adjust = form.cleaned_data['adjust']
            round = form.cleaned_data['round']
            fixed = form.cleaned_data['fixed']
            threshold = form.cleaned_data['threshold']
            print("hello")

    form = ParametersForm()

    return render(request, 'myform/form.html', {'form': form})
