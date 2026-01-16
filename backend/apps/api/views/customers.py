from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.customers.models import Customer
from apps.api.serializers.customers import (
    CustomerSerializer,
    CustomerListSerializer,
    CustomerCreateUpdateSerializer
)
from apps.shared.permissions_drf import CanManageCustomersPermission

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        summary="Lista clientes",
        description="Retorna lista paginada de clientes da organização/escritório do usuário.",
        tags=['customers']
    ),
    retrieve=extend_schema(
        summary="Detalhe do cliente",
        description="Retorna detalhes completos de um cliente específico.",
        tags=['customers']
    ),
    create=extend_schema(
        summary="Criar cliente",
        description="Cria um novo cliente para a organização/escritório do usuário.",
        tags=['customers']
    ),
    update=extend_schema(
        summary="Atualizar cliente",
        description="Atualiza todos os dados de um cliente.",
        tags=['customers']
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente",
        description="Atualiza campos específicos de um cliente.",
        tags=['customers']
    ),
    destroy=extend_schema(
        summary="Remover cliente",
        description="Remove um cliente do sistema.",
        tags=['customers']
    ),
)

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar clientes (pessoas físicas e jurídicas).
    
    Todos os endpoints são automaticamente filtrados pela organização
    e escritório do usuário autenticado.
    """

    permission_classes = [CanManageCustomersPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'city', 'state']
    search_fields = ['name', 'document', 'email', 'phone']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filtra automaticamente por organização e office do request.
        """
        return Customer.objects.for_request(self.request)
    
    def get_serializer_class(self):
        """
        Usa serializers diferentes para listagem e detalhe.
        """
        if self.action == 'list':
            return CustomerListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomerCreateUpdateSerializer
        return CustomerSerializer
    
    @extend_schema(
        summary="Ativar cliente",
        description="Marca um cliente como ativo no sistema.",
        tags=['customers']
    )

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Ativa um cliente.
        """
        customer = self.get_object()
        customer.is_active = True
        customer.save()
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Desativar cliente",
        description="Marca um cliente como inativo no sistema.",
        tags=['customers']
    )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Desativa um cliente.
        """
        customer = self.get_object()
        customer.is_active = False
        customer.save()
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Processos do cliente",
        description="Lista todos os processos vinculados ao cliente.",
        tags=['customers']
    )

    @action(detail=True, methods=['get'])
    def processes(self, request, pk=None):
        """
        Lista processos vinculados ao cliente.
        """
        customer = self.get_object()
        from apps.processes.models import ProcessParty
        from apps.api.serializers.processes import ProcessListSerializer
        
        process_parties = ProcessParty.objects.filter(customer=customer)
        processes = [pp.process for pp in process_parties]
        
        serializer = ProcessListSerializer(processes, many=True, context={'request': request})
        return Response(serializer.data)