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
    permission_classes = [IsAuthenticated]

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
        patient_gene = request.data.get('patient_gene_id')
        patient_gene = Gene.objects.filter(id=patient_gene)
        patient_gene_decrypted = patient_gene[0].decrypt_sequence()

        if not patient_gene:
            return Response({"error": "Patient gene is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the latest formula
        formula = Formula.objects.order_by('-created_at').first()
        if not formula:
            return Response({"error": "No formula found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all doctor genes
        doctor_genes = Gene.objects.filter(uploaded_by__role='doctor')

        results = []
        for doctor_gene in doctor_genes:
            decrypted_sequence = doctor_gene.decrypt_sequence()  # Decrypt the gene sequence
            similarity = self.calculate_gene_similarity(patient_gene_decrypted, decrypted_sequence, formula.formula)
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

    def calculate_gene_similarity(self, patient_gene, doctor_gene, formula):
        patient_genes = set(re.findall(r'\w+', patient_gene.upper()))
        doctor_genes = set(re.findall(r'\w+', doctor_gene.upper()))

        intersect = len(patient_genes.intersection(doctor_genes))
        n = len(doctor_genes)

        # Parse and evaluate the formula
        c = 2  # You can adjust this constant as needed
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