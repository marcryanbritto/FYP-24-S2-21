# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountSerializer, CreateAccountSerializer
from .models import Account, GeneData
from .forms import FileUploadForm

# Account Class API View that lists JSON Account Object
# To access: /api/account
class AccountView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# Account Class Creation based on form data
class CreateAccountView(APIView):
    serializer_class = CreateAccountSerializer

    # Account created with POST request
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        # If nothing wrong with data received from POST
        if serializer.is_valid():
            name = serializer.data.get('name')
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            role = serializer.data.get('role')
            email = serializer.data.get('email')

            # Check if username already exists in db
            queryset = Account.objects.filter(username=username)
            if queryset.exists():
                # For debugging purpose to identify accounts only!!
                account = queryset[0]
                return Response(AccountSerializer(account).data, status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                # Else create new room
                account = Account(name = name, 
                            username = username, 
                            password = password,
                            role = role,
                            email = email)
                account.save()
            
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
    
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# class CustomLoginView(LoginView):
#     template_name = 'DiseaseRiskCalculator/login.html' # to change to filename

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomLoginView(View):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         email = data.get('email')
#         password = data.get('password')

#         # Authenticate the user
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message": "Login successful"})
#         else:
#             return JsonResponse({"message": "Invalid credentials"}, status=400)

class CustomLogoutView(LogoutView):
    template_name = 'DiseaseRiskCalculator/logout.html' # to change to filename

def home(request):
    return render(request, 'DiseaseRiskCalculator/home.html') # to change to filename

@login_required
def home(request):
    return render(request, 'DiseaseRiskCalculator/home.html')

# Fetch constant, intersect and total n --> To be implemented futher later
class Risk_form(forms.Form):
    c = forms.FloatField(label='c')
    intersect = forms.FloatField(label='intersect')
    n = forms.FloatField(label='n')

# To calculate the percentage of risk
@login_required
def calculate_risk(request):
    if request.method == 'POST':
        form = Risk_form(request.POST)
        if form.is_valid():
            c = form.cleaned_data['c']
            i = form.cleaned_data['i']
            n = form.cleaned_data['n']
            risk = (c * i) / n * 100
            return render(request, 'DiseaseRiskCalculator/result.html', {'risk' : risk})
    else:
        form = Risk_form()
    return render(request, 'DiseaseRiskCalculator/calculate.html', {'form' : form})

# Encryption Form
class EncryptionForm(forms.Form):
    plaintext = forms.CharField(label='Plaintext', widget=forms.Textarea)


# AES symmetric enc
# Key is not stored in database yet --> need to update and store in database later
@login_required
def AES_encrypt(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            plaintext = form.cleaned_data['plaintext']
            key = get_random_bytes(16) # Can change to 16, 24, 32 btyes
            # Use CBC mode so that cannot tamper
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            key = base64.b64encode(key).decode('utf-8')
            return render(request, 'DiseaseRiskCalculator/result.html', {'ciphertext' : ct, 'iv' : iv, 'key' : key})
        else:
            # Need to update
            return HttpResponse('Invalid input')
    else:
        form = EncryptionForm()
    return render(request, 'DiseaseRiskCalculator/AES_encrypt.html', {'form' : form})

# DH Key Exchange
# Generate DH parameters --> need to be stored after generation?
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
application_private_key = parameters.generate_private_key()
application_public_key = application_private_key.public_key()

@login_required
def DH_key_exchange(request):
    if request.method == 'GET':
        # serialize pubkey and parameters
        public_key_bytes = application_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        p = parameters.parameter_numbers().p
        g = parameters.parameter_numbers().g

        context = {
            'public_key' : base64.b64encode(public_key_bytes).decode('utf-8'),
            'p' : p,
            'g' : g
        }
        return render(request, 'DiseaseRiskCalculator/DH_key_exchange.html', context)
    else:
        return HttpResponse('Error initiating DH process...')

# DiseaseRiskCalculator/views.py
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            for line in file:
                line = line.decode('utf-8').strip()  # Decode and strip any extra whitespace
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        name, sequence = parts
                        gene = GeneData(name=name)
                        gene.set_sequence(sequence)
                        gene.save()
            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'DiseaseRiskCalculator/upload.html', {'form': form})
