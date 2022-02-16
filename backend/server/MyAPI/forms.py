from django.forms import ModelForm, FileInput, Textarea, TextInput, NumberInput
from . models import Parameters
from django import forms

# class ParametersForm(forms.Form):
#     inputFile = forms.FileField(widget=forms.FileInput())
#     paramList = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List of parameters'}))
#     targetColumn = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Target column'}))
#     adjust = forms.FloatField(required=False, widget=forms.NumberInput())
#     round = forms.IntegerField(widget=forms.NumberInput())
#     fixed = forms.CharField(max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'Dictionary of fixed values'}))
#     threshold = forms.IntegerField(widget=forms.NumberInput())

class ParametersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Parameters
        fields = ('inputFile', 'paramList', 'targetColumn', 'adjust', 'round', 'fixed', 'threshold')
        widgets = {
            'inputFile': FileInput(),
            'paramList': Textarea(attrs={'placeholder': 'List of parameters'}),
            'targetColumn': TextInput(attrs={'placeholder': 'Target column'}),
            'adjust': NumberInput(),
            'round': NumberInput(),
            'fixed': TextInput(attrs={'placeholder': '"Key": "Value", "Key": "Value", etc.'}),
            'threshold': NumberInput(),
        }
        required = {
            'inputFile',
            'paramList',
            'targetColumn',
            'round',
            'threshold',
        }
