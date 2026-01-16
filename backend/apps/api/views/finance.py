from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.finance.models import FeeAgreement, Payment
from apps.api.serializers.finance import (
    FeeAgreementSerializer,
    FeeAgreementListSerializer,
    PaymentSerializer
)
from rest_framework.permissions import IsAuthenticated

class FeeAgreementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar contratos de honorários.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'customer']
    search_fields = ['title', 'customer__name']
    ordering_fields = ['start_date', 'amount', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return FeeAgreement.objects.for_request(self.request)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FeeAgreementListSerializer
        return FeeAgreementSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Ativa contrato.
        """
        agreement = self.get_object()
        agreement.status = 'active'
        agreement.save()
        
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """
        Suspende contrato.
        """
        agreement = self.get_object()
        agreement.status = 'suspended'
        agreement.save()
        
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """
        Lista pagamentos do contrato.
        """
        agreement = self.get_object()
        payments = agreement.payments.all()
        
        serializer = PaymentSerializer(payments, many=True, context={'request': request})
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pagamentos.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'fee_agreement']
    search_fields = ['description']
    ordering_fields = ['due_date', 'payment_date', 'amount']
    ordering = ['due_date']
    
    def get_queryset(self):
        return Payment.objects.for_request(self.request)
    
    def get_serializer_class(self):
        return PaymentSerializer
    
    @action(detail=True, methods=['post'])
    def mark_as_received(self, request, pk=None):
        """
        Marca pagamento como recebido.
        """
        payment = self.get_object()
        payment.mark_as_received()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_pending(self, request, pk=None):
        """
        Marca pagamento como pendente.
        """
        payment = self.get_object()
        payment.status = 'pending'
        payment.payment_date = None
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)