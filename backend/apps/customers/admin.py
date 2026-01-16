# apps/customers/admin.py

from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar clientes.
    """
    list_display = [
        'name',
        'type',
        'document',
        'email',
        'phone',
        'city',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'type',
        'is_active',
        'organization',
        'office',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'document',
        'email',
        'phone'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('organization', 'office', 'type', 'name', 'document')
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'phone_secondary')
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Filtros laterais
    list_per_page = 25
    
    # Ações em massa
    actions = ['activate_customers', 'deactivate_customers']
    
    def activate_customers(self, request, queryset):
        """Ativa clientes selecionados"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} cliente(s) ativado(s).')
    activate_customers.short_description = 'Ativar clientes selecionados'
    
    def deactivate_customers(self, request, queryset):
        """Desativa clientes selecionados"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} cliente(s) desativado(s).')
    deactivate_customers.short_description = 'Desativar clientes selecionados'

    autocomplete_fields = ['organization', 'office']