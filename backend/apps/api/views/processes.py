from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.processes.models import Process, ProcessParty
from apps.api.serializers.processes import (
    ProcessSerializer,
    ProcessListSerializer,
    ProcessCreateUpdateSerializer,
    ProcessPartySerializer
)
from apps.shared.permissions_drf import CanManageProcessesPermission

class ProcessViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar processos.
    """
    permission_classes = [CanManageProcessesPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['area', 'phase', 'is_active', 'is_confidential']
    search_fields = ['number', 'internal_number', 'subject', 'court']
    ordering_fields = ['number', 'created_at', 'distribution_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Process.objects.for_request(self.request)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProcessListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProcessCreateUpdateSerializer
        return ProcessSerializer
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
        Arquiva um processo.
        """
        process = self.get_object()
        process.phase = 'archived'
        process.is_active = False
        process.save()
        
        serializer = self.get_serializer(process)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Ativa um processo.
        """
        process = self.get_object()
        process.is_active = True
        process.save()
        
        serializer = self.get_serializer(process)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post'])
    def parties(self, request, pk=None):
        """
        GET: Lista partes do processo
        POST: Adiciona uma parte ao processo
        """
        process = self.get_object()
        
        if request.method == 'GET':
            parties = process.parties.all()
            serializer = ProcessPartySerializer(parties, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = ProcessPartySerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(process=process)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def deadlines(self, request, pk=None):
        """
        Lista prazos vinculados ao processo.
        """
        process = self.get_object()
        from apps.deadlines.models import Deadline
        from django.contrib.contenttypes.models import ContentType
        from apps.api.serializers.deadlines import DeadlineListSerializer
        
        ct = ContentType.objects.get_for_model(process)
        deadlines = Deadline.objects.filter(
            content_type=ct,
            object_id=process.id
        )
        
        serializer = DeadlineListSerializer(deadlines, many=True, context={'request': request})
        return Response(serializer.data)