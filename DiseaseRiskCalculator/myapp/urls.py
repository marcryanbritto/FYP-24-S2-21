# DiseaseRiskCalculator/urls.py

from django.urls import path
from .views import CustomLoginView, CustomLogoutView, home, calculate_risk

urlpatterns = [
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('calculate/', calculate_risk, name='calculate_risk'),
]

