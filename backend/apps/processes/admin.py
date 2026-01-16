# apps/processes/admin.py

from django.contrib import admin
from .models import Process, ProcessParty

class ProcessPartyInline(admin.TabularInline):
    """
    Inline para adicionar partes diretamente no processo.
    """
    model = ProcessParty
    extra = 1
    autocomplete_fields = ['customer']
    fields = ['customer', 'role', 'notes']

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar processos.
    """
    list_display = [
        'number',
        'subject',
        'area',
        'phase',
        'court',
        'parties_count',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'area',
        'phase',
        'is_active',
        'is_confidential',
        'organization',
        'office',
        'created_at'
    ]
    
    search_fields = [
        'number',
        'internal_number',
        'subject',
        'court'
    ]
    
    readonly_fields = ['created_at', 'updated_at', 'parties_count', 'deadlines_count']
    
    fieldsets = (
        ('Organização', {
            'fields': ('organization', 'office')
        }),
        ('Identificação', {
            'fields': ('number', 'internal_number')
        }),
        ('Classificação', {
            'fields': ('area', 'subject')
        }),
        ('Tribunal', {
            'fields': ('court', 'court_division')
        }),
        ('Andamento', {
            'fields': ('phase', 'distribution_date', 'value')
        }),
        ('Observações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_confidential')
        }),
        ('Estatísticas', {
            'fields': ('parties_count', 'deadlines_count'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Inline de partes
    inlines = [ProcessPartyInline]
    
    # Ações em massa
    actions = ['archive_processes', 'activate_processes']
    
    def archive_processes(self, request, queryset):
        count = queryset.update(phase='archived', is_active=False)
        self.message_user(request, f'{count} processo(s) arquivado(s).')
    archive_processes.short_description = 'Arquivar processos selecionados'
    
    def activate_processes(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} processo(s) ativado(s).')
    activate_processes.short_description = 'Ativar processos selecionados'


@admin.register(ProcessParty)
class ProcessPartyAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar partes (opcional, pois tem o inline).
    """
    list_display = ['process', 'customer', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['process__number', 'customer__name']
    autocomplete_fields = ['process', 'customer']