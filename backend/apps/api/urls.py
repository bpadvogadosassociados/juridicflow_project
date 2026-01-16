# apps/api/urls.py (atualizar)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

from apps.api.views.auth import (
    login_view,
    logout_view,
    me_view,
    refresh_token_view
)
from apps.api.views.customers import CustomerViewSet
from apps.api.views.processes import ProcessViewSet
from apps.api.views.deadlines import DeadlineViewSet
from apps.api.views.documents import DocumentViewSet
from apps.api.views.finance import FeeAgreementViewSet, PaymentViewSet

app_name = 'api'

# Router para ViewSets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'processes', ProcessViewSet, basename='process')
router.register(r'deadlines', DeadlineViewSet, basename='deadline')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'fee-agreements', FeeAgreementViewSet, basename='fee-agreement')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # ===== DOCUMENTAÇÃO =====
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
    
    # ===== AUTH =====
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', me_view, name='me'),
    path('auth/refresh/', refresh_token_view, name='refresh'),
    
    # ===== RECURSOS =====
    path('', include(router.urls)),
]