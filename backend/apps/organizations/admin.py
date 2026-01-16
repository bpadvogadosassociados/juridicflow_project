from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'document',
        'plan',
        'is_active',
        'total_offices',
        'total_users',
        'created_at'
    ]
    
    list_filter = ['plan', 'is_active', 'created_at']
    
    search_fields = ['name', 'document']
    
    readonly_fields = ['created_at', 'updated_at', 'total_offices', 'total_users']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'document')
        }),
        ('Plano e Status', {
            'fields': ('plan', 'is_active')
        }),
        ('Configurações', {
            'fields': ('settings',),
            'classes': ('collapse',)  
        }),
        ('Estatísticas', {
            'fields': ('total_offices', 'total_users'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_offices(self, obj):
        return obj.total_offices
    total_offices.short_description = 'Escritórios'
    
    def total_users(self, obj):
        return obj.total_users

    total_users.short_description = 'Usuários'
