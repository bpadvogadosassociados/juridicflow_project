# apps/shared/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin para visualizar logs de auditoria.
    Somente leitura.
    """
    list_display = [
        'timestamp',
        'user',
        'action_badge',
        'model_name',
        'object_repr',
        'organization',
        'office',
        'ip_address'
    ]
    
    list_filter = [
        'action',
        'model_name',
        'organization',
        'office',
        'timestamp',
        'user'
    ]
    
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'object_repr',
        'ip_address'
    ]
    
    readonly_fields = [
        'user',
        'organization',
        'office',
        'action',
        'model_name',
        'object_id',
        'object_repr',
        'changes_formatted',
        'ip_address',
        'user_agent',
        'timestamp'
    ]
    
    fieldsets = (
        ('Quem', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('Onde', {
            'fields': ('organization', 'office')
        }),
        ('O quê', {
            'fields': ('action', 'model_name', 'object_id', 'object_repr')
        }),
        ('Detalhes', {
            'fields': ('changes_formatted',)
        }),
        ('Quando', {
            'fields': ('timestamp',)
        }),
    )
    
    date_hierarchy = 'timestamp'
    
    # Somente leitura - não permite edição
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Apenas superuser pode deletar logs
        return request.user.is_superuser
    
    def action_badge(self, obj):
        """Badge colorido para ação"""
        colors = {
            'create': '#28a745',
            'update': '#ffc107',
            'delete': '#dc3545',
            'view': '#0d6efd',
            'download': '#6c757d',
            'login': '#0dcaf0',
            'logout': '#6c757d',
        }
        color = colors.get(obj.action, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_badge.short_description = 'Ação'
    
    def changes_formatted(self, obj):
        """Formata JSON de mudanças de forma legível"""
        if not obj.changes:
            return '-'
        
        try:
            html = '<table style="width: 100%; border-collapse: collapse;">'
            html += '<tr style="background: #f8f9fa;"><th style="padding: 8px; text-align: left;">Campo</th><th style="padding: 8px; text-align: left;">Antes</th><th style="padding: 8px; text-align: left;">Depois</th></tr>'
            
            for field, change in obj.changes.items():
                if field == 'action':
                    continue
                
                old = change.get('old', '-')
                new = change.get('new', '-')
                
                html += f'<tr style="border-bottom: 1px solid #dee2e6;">'
                html += f'<td style="padding: 8px;"><strong>{field}</strong></td>'
                html += f'<td style="padding: 8px; color: #dc3545;">{old}</td>'
                html += f'<td style="padding: 8px; color: #28a745;">{new}</td>'
                html += '</tr>'
            
            html += '</table>'
            return mark_safe(html)
        except:
            return format_html('<pre>{}</pre>', json.dumps(obj.changes, indent=2))
    
    changes_formatted.short_description = 'Alterações'