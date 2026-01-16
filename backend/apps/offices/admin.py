from django.contrib import admin
from .models import Office

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar escritórios.
    Platform admin pode criar/editar escritórios de qualquer organização.
    """
    list_display = [
        'name',
        'organization',
        'is_active',
        'created_at'
    ]
    
    list_filter = ['is_active', 'organization', 'created_at']
    
    search_fields = ['name', 'organization__name']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('organization', 'name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Configurações', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Organização por padrão (melhora UX)
    autocomplete_fields = []  # Se quiser, adiciona autocomplete depois