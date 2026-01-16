from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from apps.documents.models import Document
from apps.api.serializers.documents import (
    DocumentSerializer,
    DocumentListSerializer,
    DocumentUploadSerializer
)
from apps.shared.permissions_drf import CanViewConfidentialPermission
from rest_framework.permissions import IsAuthenticated

class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar documentos.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_confidential']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Document.objects.for_request(self.request)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DocumentUploadSerializer
        return DocumentSerializer
    
    def get_permissions(self):
        """
        Adiciona permissão de confidencialidade para objetos específicos.
        """
        permissions = super().get_permissions()
        
        # Para visualização de documentos confidenciais
        if self.action == 'retrieve':
            permissions.append(CanViewConfidentialPermission())
        
        return permissions
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download do arquivo.
        """
        document = self.get_object()
        
        # Verifica permissão de confidencialidade
        if document.is_confidential:
            permission = CanViewConfidentialPermission()
            if not permission.has_object_permission(request, self, document):
                return Response(
                    {'detail': 'Você não tem permissão para acessar este documento.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        from django.http import FileResponse
        return FileResponse(document.file.open('rb'), as_attachment=True)