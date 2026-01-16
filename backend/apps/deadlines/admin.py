# apps/deadlines/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Deadline

@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar prazos.
    """
    list_display = [
        'title',
        'due_date',
        'due_time',
        'priority_badge',
        'status_badge',
        'responsible',
        'days_remaining_display',
        'created_at'
    ]
    
    list_filter = [
        'type',
        'priority',
        'status',
        'due_date',
        'organization',
        'office',
        'responsible',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'responsible__email',
        'responsible__first_name',
        'responsible__last_name'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'completed_at',
        'is_overdue',
        'days_remaining',
        'alert_sent'
    ]
    
    fieldsets = (
        ('Organização', {
            'fields': ('organization', 'office')
        }),
        ('Informações Básicas', {
            'fields': ('title', 'description', 'type')
        }),
        ('Data e Hora', {
            'fields': ('due_date', 'due_time')
        }),
        ('Responsável', {
            'fields': ('responsible',)
        }),
        ('Prioridade e Status', {
            'fields': ('priority', 'status', 'completed_at')
        }),
        ('Vinculação', {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',),
            'description': 'Vincular a um processo, contrato, etc.'
        }),
        ('Alertas', {
            'fields': ('alert_days_before', 'alert_sent'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Informações Adicionais', {
            'fields': ('is_overdue', 'days_remaining', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Filtros laterais
    date_hierarchy = 'due_date'
    
    # Ações em massa
    actions = [
        'mark_as_completed',
        'mark_as_pending',
        'mark_as_cancelled'
    ]
    
    def priority_badge(self, obj):
        """Badge colorido para prioridade"""
        colors = {
            'low': '#28a745',      # Verde
            'medium': '#ffc107',   # Amarelo
            'high': '#fd7e14',     # Laranja
            'urgent': '#dc3545',   # Vermelho
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Prioridade'
    
    def status_badge(self, obj):
        """Badge colorido para status"""
        colors = {
            'pending': '#6c757d',      # Cinza
            'in_progress': '#007bff',  # Azul
            'completed': '#28a745',    # Verde
            'cancelled': '#6c757d',    # Cinza
            'overdue': '#dc3545',      # Vermelho
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def days_remaining_display(self, obj):
        """Mostra dias restantes com cor"""
        days = obj.days_remaining
        if days is None:
            return '-'
        
        if days < 0:
            color = '#dc3545'  # Vermelho
            text = f'{abs(days)} dias atrasado'
        elif days == 0:
            color = '#ffc107'  # Amarelo
            text = 'Vence hoje!'
        elif days <= 3:
            color = '#fd7e14'  # Laranja
            text = f'{days} dias'
        else:
            color = '#28a745'  # Verde
            text = f'{days} dias'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            text
        )
    days_remaining_display.short_description = 'Dias Restantes'
    
    def mark_as_completed(self, request, queryset):
        """Marca como concluído"""
        for deadline in queryset:
            deadline.mark_as_completed()
        count = queryset.count()
        self.message_user(request, f'{count} prazo(s) marcado(s) como concluído(s).')
    mark_as_completed.short_description = 'Marcar como concluído'
    
    def mark_as_pending(self, request, queryset):
        """Marca como pendente"""
        count = queryset.update(status='pending', completed_at=None)
        self.message_user(request, f'{count} prazo(s) marcado(s) como pendente(s).')
    mark_as_pending.short_description = 'Marcar como pendente'
    
    def mark_as_cancelled(self, request, queryset):
        """Marca como cancelado"""
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} prazo(s) cancelado(s).')
    mark_as_cancelled.short_description = 'Cancelar prazos'