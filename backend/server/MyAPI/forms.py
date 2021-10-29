from django.forms import ModelForm, Form
from . models import Parameters
from django import forms

class ParametersForm(forms.Form):
    inputFile = forms.FileField(widget=forms.FileInput())
    paramList = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List of parameters'}))
    targetColumn = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Target column'}))
    adjust = forms.FloatField(required=False, widget=forms.NumberInput())
    round = forms.IntegerField(widget=forms.NumberInput())
    fixed = forms.CharField(max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'Dictionary of fixed values'}))
    threshold = forms.IntegerField(widget=forms.NumberInput())

# class ParametersForm(ModelForm):
#     class Meta:
#         model = Parameters
#         fields = '__all__'
