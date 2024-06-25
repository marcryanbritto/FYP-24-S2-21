# DiseaseRiskCalcultor/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django import forms


class CustomLoginView(LoginView):
    template_name = 'DiseaseRiskCalculator/login.html' # to change to filename

class CustomLogoutView(LogoutView):
    template_name = 'DiseaseRiskCalculator/logout.html' # to change to filename

def home(request):
    return render(request, 'DiseaseRiskCalculator/home.html') # to change to filename

@login_required
def home(request):
    return render(request, 'DiseaseRiskCalculator/home.html')

class Risk_form(forms.Form):
    c = forms.FloatField(label='c')
    intersect = forms.FloatField(label='intersect')
    n = forms.FloatField(label='n')

@login_required
def Calculate_risk(request):
    if request.method == 'POST':
        form = Risk_form(request.POST)
        if form.is_valid():
            c = form.cleaned_data['c']
            i = form.cleaned_data['i']
            n = form.cleaned_data['n']
            risk = (c * i) / n * 100
            return render(request, 'DiseaseRiskCalculator/result.html', {'risk': risk})
    else:
        form = Risk_form()
    return render(request, 'DiseaseRiskCalculator/calculate.html', {'form': form})
