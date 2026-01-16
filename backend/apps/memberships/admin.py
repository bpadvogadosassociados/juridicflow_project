# apps/memberships/admin.py

from django.contrib import admin
from .models import Membership

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar memberships (vínculos user-org-office).
    """
    list_display = [
        'user',
        'organization',
        'office',
        'role',
        'is_active',
        'created_at'
    ]
    
    list_filter = ['role', 'is_active', 'organization', 'created_at']
    
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'organization__name',
        'office__name'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Vínculo', {
            'fields': ('user', 'organization', 'office', 'role')
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
    
    # Facilita busca
    autocomplete_fields = ['user', 'organization', 'office']
