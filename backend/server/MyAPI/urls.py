from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('input', views.ParametersView)
router.register('results-nnls', views.ResultsNNLSView)
router.register('results-ols', views.ResultsOLSView)

urlpatterns = [
    path('form/', views.myform, name='myform'),
    path('api/', include(router.urls)),
]
