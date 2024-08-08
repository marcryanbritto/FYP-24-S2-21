# views.py
from rest_framework import viewsets, status
import re
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from .models import User, UserActivity, Gene, Formula
from .serializers import UserSerializer, UserCreateSerializer, GeneSerializer, GeneFileUploadSerializer, GeneTextInputSerializer, Gene, UserActivitySerializer, FormulaSerializer

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Generate DH parameters
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

def generate_private_key():
    return parameters.generate_private_key()

def generate_public_key(private_key):
    return private_key.public_key()

def load_public_key(public_bytes):
    return serialization.load_pem_public_key(public_bytes, backend=default_backend())

def compute_shared_secret(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'gene comparison',
        backend=default_backend()
    ).derive(shared_key)
    return derived_key

def encrypt_message(key, message):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return iv + encryptor.update(message.encode()) + encryptor.finalize()

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_message[16:]) + decryptor.finalize()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        role = serializer.validated_data.get('role')
        
        if role == 'doctor' and not request.user.is_staff:
            return Response({"error": "Only admins can register doctors."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        self.perform_create(serializer)
        # Make newly created admins is_staff flag set to True
        user = User.objects.get(email=serializer.data['email'])
        if user.role == 'admin':
            user.is_staff = True
            user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            UserActivity.objects.create(user=user, action='login')
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            UserActivity.objects.create(user=request.user, action='logout')
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def set_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = request.data.get('is_active', user.is_active)
        user.save()
        return Response(UserSerializer(user).data)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def deactivate_patient(self, request, pk=None):
        user = self.get_object()
        if user.role != 'patient':
            return Response({"error": "This action is only for patients."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PatientRegistrationView(viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['role'] != 'patient':
            return Response({"error": "This endpoint is for patient registration only."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        UserActivity.objects.create(user=user, action='register_patient')
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['post'])
    def upload(self, request):
        name = request.data.get('name')
        sequence = request.data.get('sequence')
        file = request.FILES.get('file')

        if file:
            if file.name.endswith('.txt'):
                content = file.read().decode('utf-8')
                sequence = content.strip()
            else:
                return Response(
                    {"detail": "Only .txt files are allowed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not name or not sequence:
            return Response(
                {"detail": "Name and sequence are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_by = request.user
        gene = Gene.objects.create(name=name, sequence=sequence, uploaded_by=uploaded_by)
        serializer = self.get_serializer(gene)
        UserActivity.objects.create(user=request.user, action='create_gene')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_genes(self, request):
        user = request.user
        genes = Gene.objects.filter(uploaded_by=user)
        page = self.paginate_queryset(genes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(genes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_gene(self, request):
        gene_id = request.data.get('gene_id')
        if not gene_id:
            return Response({"error": "Gene ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        gene = Gene.objects.filter(id=gene_id, uploaded_by=request.user).first()
        if not gene:
            return Response({"error": "Gene not found."}, status=status.HTTP_404_NOT_FOUND)
        
        gene.delete()
        UserActivity.objects.create(user=request.user, action='delete_gene')
        return Response({"detail": "Gene deleted."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def edit_gene(self, request):
        gene_id = request.data.get('gene_id')
        name = request.data.get('name')
        sequence = request.data.get('sequence')
        
        if not gene_id:
            return Response({"error": "Gene ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        gene = Gene.objects.filter(id=gene_id, uploaded_by=request.user).first()

        # Check if gene exists
        if not gene:
            return Response({"error": "Gene not found."}, status=status.HTTP_404_NOT_FOUND)
        
        decrypted_sequence = gene.decrypt_sequence()
        if name:
            gene.name = name
        if sequence:
            gene.sequence = sequence  # Encrypt sequence before saving

        try:
            with transaction.atomic():
                gene.save()
                UserActivity.objects.create(user=request.user, action='edit_gene')
                return Response(GeneSerializer(gene).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='get_my_gene')
    def get_my_gene(self, request, pk=None):
        gene = Gene.objects.filter(id=pk, uploaded_by=request.user).first()
        if not gene:
            return Response({"error": "Gene not found or you do not have permission to view it."}, status=status.HTTP_404_NOT_FOUND)
        return Response(GeneSerializer(gene).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def calculate_similarity(self, request):
        # Log the request data
        print("Received request data:", request.data)
        
        patient_gene_id = request.data.get('patient_gene_id')
        if not patient_gene_id:
            print("Error: Patient gene ID is required.")
            return Response({"error": "Patient gene ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        patient_gene = Gene.objects.filter(id=patient_gene_id).first()
        if not patient_gene:
            print("Error: Patient gene not found.")
            return Response({"error": "Patient gene not found."}, status=status.HTTP_404_NOT_FOUND)

        # Patient Keygen
        patient_private_key = generate_private_key()
        patient_public_key = generate_public_key(patient_private_key)

        # Doctor Keygen
        doctor_private_key = generate_private_key()
        doctor_public_key = generate_public_key(doctor_private_key)

        # Doctor's public key should be provided in the request
        # doctor_public_key_bytes = request.data.get('doctor_public_key')
        # if not doctor_public_key_bytes:
        #     print("Error: Doctor's public key is required.")
        #     return Response({"error": "Doctor's public key is required."}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     doctor_public_key = load_public_key(doctor_public_key_bytes)
        # except Exception as e:
        #     print("Error loading doctor's public key:", e)
        #     return Response({"error": "Invalid doctor's public key."}, status=status.HTTP_400_BAD_REQUEST)

        # Compute shared secret
        shared_key = compute_shared_secret(patient_private_key, doctor_public_key)

        patient_gene_decrypted = patient_gene.decrypt_sequence()
        patient_gene_encrypted = encrypt_message(shared_key, patient_gene_decrypted)

        # Print encrypted and decrypted strings for debugging
        print("Encrypted patient gene sequence:", patient_gene_encrypted)
        dec_test = decrypt_message(shared_key, patient_gene_encrypted)
        print("Decrypted patient gene sequence:", dec_test.decode())

        # Get the latest formula
        formula = Formula.objects.order_by('-created_at').first()
        if not formula:
            print("Error: No formula found.")
            return Response({"error": "No formula found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all doctor genes
        doctor_genes = Gene.objects.filter(uploaded_by__role='doctor')

        results = []
        for doctor_gene in doctor_genes:
            decrypted_sequence = doctor_gene.decrypt_sequence()
            doctor_gene_encrypted = encrypt_message(shared_key, decrypted_sequence)
            
            # Print encrypted and decrypted strings for doctor gene
            print("Encrypted doctor gene sequence:", doctor_gene_encrypted)
            decrypted_doctor_test = decrypt_message(shared_key, doctor_gene_encrypted)
            print("Decrypted doctor gene sequence (for verification):", decrypted_doctor_test.decode())

            similarity = self.calculate_gene_similarity(shared_key, patient_gene_encrypted, doctor_gene_encrypted, formula.formula)
            if similarity >= 0.5:
                results.append({
                    'doctor_email': doctor_gene.uploaded_by.email,
                    'gene_name': doctor_gene.name,
                    'similarity': similarity
                })

        # Sort results by similarity in descending order
        results.sort(key=lambda x: x['similarity'], reverse=True)
        UserActivity.objects.create(user=request.user, action='calculate_similarity')
        return Response(results, status=status.HTTP_200_OK)

    def calculate_gene_similarity(self, shared_key, patient_gene_encrypted, doctor_gene_encrypted, formula):
        patient_genes = set(re.findall(r'\w+', decrypt_message(shared_key, patient_gene_encrypted).decode().upper()))
        doctor_genes = set(re.findall(r'\w+', decrypt_message(shared_key, doctor_gene_encrypted).decode().upper()))

        intersect = len(patient_genes.intersection(doctor_genes))
        n = len(doctor_genes)

        # Parse and evaluate the formula
        similarity = eval(formula.replace('intersect', str(intersect)).replace('n', str(n)))

        return round(similarity, 2)



class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivity.objects.all().order_by('-timestamp')
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]

class FormulaViewSet(viewsets.ModelViewSet):
    queryset = Formula.objects.all()
    serializer_class = FormulaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only one formula is returned
        return Formula.objects.order_by('-created_at')[:1]
    
    ## Upload a formula only for Doctors or Admins
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_formula(self, request):
        if request.user.role == 'patient':
            return Response({"error": "Only doctors or admins can upload formulas."}, status=status.HTTP_403_FORBIDDEN)
        
        formula = request.data.get('formula')
        if not formula:
            return Response({"error": "Formula is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        Formula.objects.all().delete()
        formula = Formula.objects.create(formula=formula, created_by=request.user)
        UserActivity.objects.create(user=request.user, action='upload_formula')
        return Response(FormulaSerializer(formula).data, status=status.HTTP_201_CREATED)