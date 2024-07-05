# api/urls.py
# Store URLs local to the app

from django.urls import path
from django.views.generic import TemplateView
from .views import CustomLoginView, CustomLogoutView, home, calculate_risk, AES_encrypt, DH_key_exchange, upload_file
from .views import AccountView, CreateAccountView

urlpatterns = [
    path('', home, name='home'),
    path('account', AccountView.as_view()),
    path('create-account', CreateAccountView.as_view()),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('calculate/', calculate_risk, name='calculate_risk'),
    path('aes_encrypt/', AES_encrypt, name='aes_encrypt'),
    path('dh_key_exchange/', DH_key_exchange, name='dh_key_exchange'),
    path('upload/', upload_file, name='upload_file'),
    path('upload_success/', TemplateView.as_view(template_name='DiseaseRiskCalculator/upload_success.html'), name='upload_success'),
]

