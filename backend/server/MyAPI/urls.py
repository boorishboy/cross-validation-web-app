from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('input', views.InputView, basename = 'input')
router.register('results', views.ResultsView, basename = 'results')
router.register('combined', views.CombinedView, basename = 'combined')


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='result-dashboard'),
    path('new-run/', views.input, name='input'),
    path('api/', include(router.urls)),
    path('result-detail/<int:pk>/', views.ResultDetailView.as_view(), name='result-detail'),
]
