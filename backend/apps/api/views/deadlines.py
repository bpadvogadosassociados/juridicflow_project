from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.deadlines.models import Deadline
from apps.api.serializers.deadlines import (
    DeadlineSerializer,
    DeadlineListSerializer,
    DeadlineCreateUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated

class DeadlineViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar prazos.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'priority', 'status', 'responsible']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['due_date']
    
    def get_queryset(self):
        return Deadline.objects.for_request(self.request)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeadlineListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DeadlineCreateUpdateSerializer
        return DeadlineSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Marca prazo como concluído.
        """
        deadline = self.get_object()
        deadline.mark_as_completed()
        
        serializer = self.get_serializer(deadline)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancela um prazo.
        """
        deadline = self.get_object()
        deadline.status = 'cancelled'
        deadline.save()
        
        serializer = self.get_serializer(deadline)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """
        Lista prazos atrasados.
        """
        queryset = self.get_queryset().filter(
            status='overdue'
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Lista prazos dos próximos 7 dias.
        """
        today = timezone.now().date()
        next_week = today + timezone.timedelta(days=7)
        
        queryset = self.get_queryset().filter(
            due_date__gte=today,
            due_date__lte=next_week,
            status='pending'
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)