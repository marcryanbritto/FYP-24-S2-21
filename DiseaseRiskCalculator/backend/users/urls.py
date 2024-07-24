from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PatientRegistrationView, GeneViewSet, UserActivityViewSet, FormulaViewSet, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patient-registration', PatientRegistrationView, basename='patient-registration')
router.register(r'genes', GeneViewSet)
router.register(r'user-activity', UserActivityViewSet, basename='user-activity')
router.register(r'formulas', FormulaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]