# api/urls.py
# Store URLs local to the app

from django.urls import path
from .views import CustomLoginView, CustomLogoutView, home, calculate_risk, AES_encrypt, DH_key_exchange

urlpatterns = [
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('calculate/', calculate_risk, name='calculate_risk'),
    path('aes_encrypt/', AES_encrypt, name='aes_encrypt'),
    path('dh_key_exchange/', DH_key_exchange, name='dh_key_exchange'),
]

