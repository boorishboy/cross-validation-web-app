from django.contrib import admin
from .models import Parameters, ResultsNNLS, ResultsOLS
# Register your models here.
admin.site.register(Parameters)
admin.site.register(ResultsOLS)
admin.site.register(ResultsNNLS)
