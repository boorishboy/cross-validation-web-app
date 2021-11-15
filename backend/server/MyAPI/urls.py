from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('input', views.ParametersView)
router.register('results', views.ResultsView)


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='result-dashboard'),
    path('form/', views.myform, name='myform'),
    path('api/', include(router.urls)),
    path('result-detail', views.ResultDetailView.as_view(), name='result-detail'),
]
